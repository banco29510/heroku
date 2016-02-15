from __future__ import absolute_import

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout, authenticate, login
from django.core.urlresolvers import reverse
from django.db import models
from django.core.files.base import ContentFile
from django.core.files import File as DjangoFile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404, get_list_or_404, redirect, render
from django.contrib.auth import authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic.edit import *
from django.conf import settings

import os, sys, glob, mimetypes, re, logging, pickle, tempfile, time, subprocess, json, base64, pprint, hashlib, shutil
from datetime import datetime
from subprocess import *
from shutil import *

from djcelery import celery
from score.celery import *
from celery import Task
import gitlab

from repository.models import *

from git import Repo, Actor, Head, Remote, Git, Blob, Tree



# \brief     
@app.task
def ampq_deleteDownload():
    
    repository = get_object_or_404(Repository, pk=id)
    temp = tempfile.mkdtemp()
    
    repo = Repo.clone_from(repository.url, temp, branch=branch) # clone du dépot
  
   
    file.file.delete()
    file.delete()

    return 1
    



