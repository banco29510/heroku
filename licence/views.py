# -*- coding: utf-8 -*-
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
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.utils.decorators import method_decorator
from django.utils.functional import lazy
from django.core.urlresolvers import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required

import os, sys, datetime, glob, shutil, mimetypes, re, logging, pickle


from licence.models import Licence
from licence.forms import *

##
# \brief Page
# \author A. H.
# \fn def
# \return
#
@login_required
def listLicences(request,):

    licences = Licence.objects.all()

    paginator = Paginator(licences, 20)

    page = request.GET.get('page', 1)
    try:
        licences = paginator.page(page)
    except PageNotAnInteger:
        licences = paginator.page(1)
    except EmptyPage:
        licences = paginator.page(paginator.num_pages)


    return render(request, "licence/list.html", {'licences': licences,})


##
# \brief Page detail dépot
# \author A. H.
# \fn def
# \return
#
@login_required
def detailLicence(request, pk=None):

    licence = Licence.objects.get(pk=pk)

    return render(request, "licence/detail.html", {'licence': licence,})



##
# \brief Page de recherche des partitions
# \author A. H.
# \fn def
# \return
#
@login_required
@staff_member_required
def createLicence(request):

    if request.method == 'POST':
        form = CreateLicenceForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']

            licence = Licence(name=name,)

            licence.save()

            messages.add_message(request, messages.INFO, 'La licence à été créé')
            return redirect('licence-list', )

        else:
            pass

    else:
        form = CreateLicenceForm()


    return render(request, "licence/create.html", {'form': form,})

##
# \brief Page de
# \author A. H.
# \fn def
# \return
#
@login_required
@staff_member_required
def updateLicence(request, pk=None):

    licence = Licence.objects.get(pk=pk)

    if request.method == 'POST':
        form = CreateLicenceForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']

            licence.name = name

            licence.save()

            messages.add_message(request, messages.INFO, 'La licence à été modifié')
            return redirect('licence-list', )

        else:
            pass

    else:
        form = UpdateLicenceForm(initial={'name':licence.name,})


    return render(request, "licence/update.html", {'form': form,})


##
# \brief Page de
# \author A. H.
# \fn def
# \return
#
@login_required
@staff_member_required
def deleteLicence(request, pk=None):

    licence = Licence.objects.get(pk=pk)

    if request.method == 'POST':
        form = DeleteLicenceForm(request.POST)

        if form.is_valid():

            licence.delete()

            messages.add_message(request, messages.INFO, 'La licence à été suprimé')
            return redirect('licence-list', )

        else:
            pass
    else:
        form = DeleteLicenceForm()

    return render(request, "licence/confirm_delete.html", {'form': form,})



