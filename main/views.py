from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.core.urlresolvers import reverse
from django.db import models
from django.core.files.base import ContentFile
from django.core.files import File as File
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.auth import authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from repository.models import *
from .forms import *


#@cache_page(60 * 5) # cache pendant 5 minutes
def main(request):
    
    commits = Commit.objects.all().order_by('-date')
    list_commits = []
    i = 0
    
    for commit in commits:
        if i != 5:
            list_commits.append(commit)
        i += 1
        
        
    paginator = Paginator(list_commits, 5)

    page = request.GET.get('page', 1)
    try:
        list_commits = paginator.page(page)
    except PageNotAnInteger:
        list_commits = paginator.page(1)
    except EmptyPage:
        list_commits = paginator.page(paginator.num_pages)
    
    return render(request, 'main/main.html', {'commits': list_commits})

#@cache_page(60 * 5) # cache pendant 5 minutes
def cgu(request):
    return render(request, 'main/cgu.html', {})

# Affiche la page pour l'utilisateur
@login_required
def profile(request):
    return render(request, 'main/profile.html', {'user': request.user,})
    
    
# \brief modifie les informations de l'utilisateur
@login_required
def editUser(request):
    
    if request.method == 'POST':
        form = EditUserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            
            request.user.firstName = firstName
            request.user.lastName = lastName
            request.user.username = username
            
            request.user.save()
            

            return redirect('main-profile',)

    else:

        form = EditUserForm(initial={'username': request.user.username, 'firstName': request.user.first_name, 'lastName': request.user.last_name,})

    
    return render(request, 'main/editUser.html', {'user': request.user, 'form': form})
    
# \brief desinscrit l'utilisateur
@login_required
def unregister(request):
    
    logout()
    request.user.delete()
    return redirect('main')
    
