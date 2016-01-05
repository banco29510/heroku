##
# \file views.py
# \brief Liste des actions de base pour les logiciels
# \date 02/05/15
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


from software.models import Software
from software.forms import *

##
# \brief Liste des logiciels
# \author A. H.
# \fn def listSoftwares(request):
# \return software/list.html
#
@login_required
def listSoftwares(request):

    softwares = Software.objects.all()

    paginator = Paginator(softwares, 20)

    page = request.GET.get('page', 1)
    try:
        softwares = paginator.page(page)
    except PageNotAnInteger:
        softwares = paginator.page(1)
    except EmptyPage:
        softwares = paginator.page(paginator.num_pages)


    return render(request, "software/list.html", {'softwares': softwares,})


##
# \brief Page detail dépot
# \author A. H.
# \fn def detailSoftware(request, pk=None):
# \return software/detail.html
#
@login_required
def detailSoftware(request, pk=None):

    software = Software.objects.get(pk=pk)

    return render(request, "software/detail.html", {'software': software,})

##
# \brief Création des logiciels
# \author A. H.
# \fn def createSoftware(request):
# \return software/create.html ou redirection software-list
#
@login_required
@staff_member_required
def createSoftware(request):

    if request.method == 'POST':
        form = CreateSoftwareForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            extension = form.cleaned_data['extension']
            licence = form.cleaned_data['licence']


            software = Software(name=name, extension=extension, licence=licence)

            software.save()

            messages.add_message(request, messages.INFO, 'Le logiciel à été créé')
            return redirect('software-list', )

        else:
            pass

    else:
        form = CreateSoftwareForm()


    return render(request, "software/create.html", {'form': form,})

##
# \brief Page de mise à jour des logiciels
# \author A. H.
# \fn def updateSoftware(request, pk=None):
# \return software/update.html ou redirection software-list
#
@login_required
@staff_member_required
def updateSoftware(request, pk=None):

    software = Software.objects.get(pk=pk)

    if request.method == 'POST':
        form = CreateSoftwareForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']
            extension = form.cleaned_data['extension']
            licence = form.cleaned_data['licence']


            software.name = name.capitalize()
            software.extension = extension
            software.licence = licence

            software.save()

            messages.add_message(request, messages.INFO, 'Le logiciel à été modifié')
            return redirect('software-list', )

        else:
            pass

    else:
        form = UpdateSoftwareForm(initial={'name':software.name, })


    return render(request, "software/update.html", {'form': form,})


##
# \brief supression des logiciels
# \author A. H.
# \fn def deleteSoftware(request, pk=None):
# \return software/confirm_delete.html ou redirection software-list
#
@login_required
@staff_member_required
def deleteSoftware(request, pk=None):

    software = Software.objects.get(pk=pk)

    if request.method == 'POST':
        form = DeleteSoftwareForm(request.POST)

        if form.is_valid():

            software.delete()

            messages.add_message(request, messages.INFO, 'Le logiciel à été suprimé')
            return redirect('software-list', )

        else:
            pass
    else:
        form = DeleteSoftwareForm()

    return render(request, "software/confirm_delete.html", {'form': form,})


