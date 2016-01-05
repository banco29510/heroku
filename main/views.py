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


#@cache_page(60 * 5) # cache pendant 5 minutes
def main(request):
    return render(request, 'main/main.html', {})

#@cache_page(60 * 5) # cache pendant 5 minutes
def cgu(request):
    return render(request, 'main/cgu.html', {})

# Affiche la page pour l'utilisateur
@login_required
def profile(request):
    return render(request, 'main/profile.html', {'user': request.user,})
    