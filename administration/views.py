##
# \file administration.views.py
# \brief Administration du site
# \date 08 mai 2015
#
# Page en lien avec la gestion du site
#
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django import forms
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.db import models
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from django.core.management import call_command
from django.core.files import File as File
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import get_object_or_404, get_list_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q




import os, sys, datetime, glob, shutil, mimetypes, re, logging, hashlib, random, base64, pprint, tempfile, shutil
import zipfile, tarfile, bz2

import psutil

from repository.models import *

##
# \brief page d'accueil du dashboard
# \author A. H.
# \fn def dashboard(request)
# \return le dashboard
#
@login_required
@staff_member_required
@csrf_exempt
def dashboard(request):

    return render(request, 'dashboard/dashboard.html', {})


##
# \brief page informations serveur
# \author A. H.
# \fn def dashboard(request)
# \return le dashboard
#
@login_required
@staff_member_required
@csrf_exempt
def informationsServer(request):

    disk_usage_free = psutil.disk_usage('/').free
    disk_usage_total = psutil.disk_usage('/').total
    disk_usage_used = psutil.disk_usage('/').used

    memory_used = psutil.virtual_memory().used
    memory_total = psutil.virtual_memory().total

    return render(request, 'dashboard/informationsServer.html', {'disk_usage_free': disk_usage_free, 'disk_usage_total': disk_usage_total, 'disk_usage_used': disk_usage_used,
                                                                 'memory_used': memory_used, 'memory_total': memory_total,})

##
# \brief page seo
# \author A. H.
# \fn def dashboard(request)
# \return le dashboard
#
@login_required
@staff_member_required
@csrf_exempt
def seo(request):
    return render(request, 'dashboard/seo.html', {})

##
# \brief execute les commandes
# \author A. H.
# \fn def managementCommand(request):
# \return
#
@login_required
@staff_member_required
@csrf_exempt
def managementCommands(request):

    command = request.GET.get('command', None)

    if command == 'updateRepository':
        value = call_command('updateRepository')
        messages.add_message(request, messages.INFO, 'Retour de la commande : '+str(value))


    return render(request, 'dashboard/commands.html', {})








