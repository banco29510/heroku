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
        
        
    paginator = Paginator(list_commits, 20)

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
    
# Affiche la page pour se connecter
def login(request):
    
    if request.method == 'POST':
        form = LoginForm(request.POST, request.FILES)
        

        if form.is_valid():
           
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            
            user = authenticate(username=name, password=password)
            
            if user is not None:
                # the password verified for the user
                if user.is_active:
                    messages.add_message(request, messages.INFO, 'Vous êtes connecté.')
                    return redirect('main')
                else:
                    messages.add_message(request, messages.INFO, 'Votre compte à été désactivé.')
            else:
                # the authentication system was unable to verify the username and password
                messages.add_message(request, messages.INFO, 'Informations incorectes.')

    else:

        form = LoginForm(initial='',)
        

    return render(request, 'main/login.html', {'form': form})