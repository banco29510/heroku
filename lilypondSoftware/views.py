#-*- coding: utf-8 -*-
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.utils.decorators import method_decorator
from django.utils.functional import lazy
from django.core.urlresolvers import reverse_lazy
#from django.core.servers.basehttp import FileWrapper
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt

import os, sys, datetime, glob, shutil, mimetypes, re, logging, pickle, tempfile, markdown, base64, mimetypes, zipfile
import subprocess

from repository.models import *


##
# \brief Page d' édition de partitions lilypond
# \author A. H.
# \fn def main(request):
# \return lilypondSoftware/main.html
#
@login_required
def main(request):

    file = request.GET.get("file", None)
    commit = request.GET.get("commit", None)

    temporary_folder = tempfile.mkdtemp()

    if file != None:
        file = get_object_or_404(File, pk=file)
        commit = get_object_or_404(Commit, pk=commit)

        branch = request.GET.get("branch", 'master')
        repo = Repo.clone_from(commit.repository.url, temporary_folder, branch=branch)

        content = open(temporary_folder+'/'+file.name, 'r+', encoding='UTF8')
        content = content.read()

    else:
        file = None
        content = ''


    return render(request, "lilypondSoftware/main.html", {'file': file, 'content': content})


##
# \brief Page de compilation
# \author A. H.
# \fn def lilypondCompilation(request):
# \return response
#
@login_required
@csrf_exempt
def lilypondCompilation(request):

    temporary_folder = tempfile.mkdtemp()
    format = 'pdf'

    code = request.GET.get("code", None)

    open(temporary_folder+'/lilypond.pdf', 'wb+').close()

    file = open(temporary_folder+'/lilypond.ly', 'w+', encoding='UTF8')
    if code:
        file.write(str(code))
    else:
        file.write(str("""
            \include "italiano.ly"\n
            \\version "2.16.2"\n
            \header {
                title = "titre"
                subtitle = "sous titre"
                composer = "compositeur"
                dedication = "Dédicace"
                instrument = ""
                copyright = ""
            }
            {
                la'
            }


        """))

    file.close()

    #print(subprocess.call('lilypond -f '+format+' -o lilypond.pdf lilypond.ly &>tous.log lilypond.ly', shell=True, cwd=temporary_folder, universal_newlines=True))

    print(subprocess.call('lilypond -f '+format+' lilypond.ly', shell=True, cwd=temporary_folder, universal_newlines=True))

    
    response = HttpResponse()

    response['Content-Type'] = mimetype=mimetypes.guess_type('lilypond.pdf')[0]
    response['Content-Disposition'] = 'inline; filename=lilypond.pdf'
    response['Content-Length'] = os.path.getsize(temporary_folder+'/lilypond.pdf')
    response.write(open(temporary_folder+'/lilypond.pdf', 'rb').read())

    return response

##
# \brief Page d'ereurs de compilation
# \author A. H.
# \fn def lilypondErrorsCompilation(request):
# \param[in] request request Django
# \return response
#
@login_required
@csrf_exempt
def lilypondErrorsCompilation(request):

    temporary_folder = tempfile.mkdtemp()
    format = 'pdf'

    code = request.GET.get("code", None)


    open(temporary_folder+'/lilypond.pdf', 'wb+').close()

    file = open(temporary_folder+'/lilypond.ly', 'w+', encoding='UTF8')
    if code != '':
        file.write(str(code))

    file.close()

    print(subprocess.call('lilypond -f '+format+' -o lilypond.pdf lilypond.ly &>tous.log lilypond.ly', shell=True, cwd=temporary_folder, universal_newlines=True))

    file = open(temporary_folder+'/lilypond.log', 'r+', encoding='UTF8')
    log = file.read()
    log = log.replace(temporary_folder, '')
    print(log)
    file.write(log)
    file.close()


    response = HttpResponse()

    response['Content-Type'] = mimetype=mimetypes.guess_type('lilypond.log')[0]
    response['Content-Disposition'] = 'inline; filename=lilypond.log'
    response['Content-Length'] = os.path.getsize(temporary_folder+'/lilypond.log')
    response.write(open(temporary_folder+'/lilypond.log', 'rb',).read())

    return response

