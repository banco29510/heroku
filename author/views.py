# -*- coding: utf-8 -*-
##
# \file author.views.py
# \brief Page de CRUD pour les auteurs
# \date 26/03/2015
#
# Page en lien avec les auteurs
#
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
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView
from django.shortcuts import get_object_or_404, get_list_or_404
from django.utils.decorators import method_decorator
from django.utils.functional import lazy
from django.core.urlresolvers import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required


import os, sys, datetime, glob, shutil, mimetypes, re, logging, pickle


from author.models import Author

from author.forms import *

##
# \brief Liste des auteurs
# \author A. H.
# \date 26/03/2015
# \fn def listAuthors(request):
# \param[in] request Requête Django
# \return author/list.html
#
@login_required
def listAuthors(request):

    authors = Author.objects.all()

    paginator = Paginator(authors, 20)

    page = request.GET.get('page', 1)
    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        authors = paginator.page(1)
    except EmptyPage:
        authors = paginator.page(paginator.num_pages)


    return render(request, "author/list.html", {'authors': authors,})


##
# \brief Détail des dépots (partitions)
# \author A. H.
# \date 26/03/2015
# \fn def detailAuthor(request, pk=None):
# \param[in] request Requête Django
# \param[in] pk=None Id de l'auteur
# \return author/detail.html
#
@login_required
def detailAuthor(request, pk=None):

    author = Author.objects.get(pk=pk)

    return render(request, "author/detail.html", {'author': author,})

##
# \brief Formulaire de création des auteurs
# \author A. H.
# \date 26/03/2015
# \fn def createAuthor(request):
# \param[in] request Requête Django
# \return author/create.html ou redirection author-list
#
@login_required
@staff_member_required
def createAuthor(request):

    if request.method == 'POST':
        form = CreateAuthorForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            birthDate = form.cleaned_data['birthDate']
            deathDate = form.cleaned_data['deathDate']
            nationality = form.cleaned_data['nationality']

            auteur = Author(name=name, birthDate=birthDate, deathDate=deathDate, nationality=nationality)

            auteur.save()

            messages.add_message(request, messages.INFO, 'L\'auteur à été créé')
            return redirect('author-list', )

        else:
            pass

    else:
        form = CreateAuthorForm()


    return render(request, "author/create.html", {'form': form,})

##
# \brief Modification des auteurs
# \author A. H.
# \date 26/03/2015
# \fn def updateAuthor(request, pk=None):
# \param[in] request Requête Django
# \param[in] pk=None id de l'auteur
# \return author/update.html ou redirection author-list
#
@login_required
@staff_member_required
def updateAuthor(request, pk=None):

    author = Author.objects.get(pk=pk)

    if request.method == 'POST':
        form = CreateAuthorForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            birthDate = form.cleaned_data['birthDate']
            deathDate = form.cleaned_data['deathDate']
            nationality = form.cleaned_data['nationality']

            author.name = name.capitalize()
            author.deathDate = deathDate
            author.birthDate = deathDate
            author.nationality = nationality

            author.save()

            messages.add_message(request, messages.INFO, 'L\'auteur à été modifié')
            return redirect('author-list', )

        else:
            pass

    else:
        form = UpdateAuthorForm(initial={'name':author.name, 'birthDate':author.birthDate, 'deathDate':author.deathDate, 'nationality':author.nationality})


    return render(request, "author/update.html", {'form': form,})


##
# \brief Supression des auteurs
# \author A. H.
# \date 26/03/2015
# \fn def deleteAuthor(request, pk=None):
# \param[in] request Requête Django
# \param[in] pk=None Id de l'auteur
# \return author/confirm_delete.html ou redirection author-list
#
@login_required
@staff_member_required
def deleteAuthor(request, pk=None):

    author = Author.objects.get(pk=pk)

    if request.method == 'POST':
        form = DeleteAuthorForm(request.POST)

        if form.is_valid():

            author.delete()

            messages.add_message(request, messages.INFO, 'L\'auteur à été suprimé')
            return redirect('author-list', )

        else:
            pass
    else:
        form = DeleteAuthorForm()

    return render(request, "author/confirm_delete.html", {'form': form,})


