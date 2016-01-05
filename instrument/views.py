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


from instrument.models import Instrument
from instrument.forms import *

##
# \brief Page
# \author A. H.
# \fn def
# \return
#
@login_required
def listInstruments(request,):

    instruments = Instrument.objects.all()

    paginator = Paginator(instruments, 20)

    page = request.GET.get('page', 1)
    try:
        instruments = paginator.page(page)
    except PageNotAnInteger:
        instruments = paginator.page(1)
    except EmptyPage:
        instruments = paginator.page(paginator.num_pages)


    return render(request, "instrument/list.html", {'instruments': instruments,})


##
# \brief Page detail dépot
# \author A. H.
# \fn def
# \return
#
@login_required
def detailInstrument(request, pk=None):

    instrument = Instrument.objects.get(pk=pk)

    return render(request, "instrument/detail.html", {'instrument': instrument,})



##
# \brief Page de recherche des partitions
# \author A. H.
# \fn def
# \return
#
@login_required
@staff_member_required
def createInstrument(request):

    if request.method == 'POST':
        form = CreateInstrumentForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']

            instrument = Instrument(name=name,)

            instrument.save()

            messages.add_message(request, messages.INFO, 'L\'Instrument à été créé')
            return redirect('instrument-list', )

        else:
            pass

    else:
        form = CreateInstrumentForm()


    return render(request, "instrument/create.html", {'form': form,})

##
# \brief Page de
# \author A. H.
# \fn def
# \return
#
@login_required
@staff_member_required
def updateInstrument(request, pk=None):

    instrument = Instrument.objects.get(pk=pk)

    if request.method == 'POST':
        form = CreateInstrumentForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data['name']

            instrument.name = name

            instrument.save()

            messages.add_message(request, messages.INFO, 'L\'instrument à été modifié')
            return redirect('instrument-list', )

        else:
            pass

    else:
        form = UpdateInstrumentForm(initial={'name':instrument.name,})


    return render(request, "instrument/update.html", {'form': form,})


##
# \brief Page de
# \author A. H.
# \fn def
# \return
#
@login_required
@staff_member_required
def deleteInstrument(request, pk=None):

    instrument = Instrument.objects.get(pk=pk)

    if request.method == 'POST':
        form = DeleteInstrumentForm(request.POST)

        if form.is_valid():

            instrument.delete()

            messages.add_message(request, messages.INFO, 'L\'instrument à été suprimé')
            return redirect('instrument-list', )

        else:
            pass
    else:
        form = DeleteInstrumentForm()

    return render(request, "instrument/confirm_delete.html", {'form': form,})


