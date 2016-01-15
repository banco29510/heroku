# -*- coding: utf-8 -*-
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

import os, sys, datetime, glob, mimetypes, re, logging, pickle, tempfile, time, subprocess, json, base64, pprint
from shutil import *

from djcelery import celery
from score.celery import *
from celery import Task
import gitlab

from repository.models import *
        

@app.task
def ampq_addFile(gitlabId=None, file=None, message=None, branch="master"):
    
    git = gitlab.Gitlab(settings.GITLAB_URL, settings.GITLAB_TOKEN)
        
    git.createfile(gitlabId, os.path.basename(file.file.name), branch, file.file.read(), message)
    #pprint.pprint(file)
    
    file.file.delete()
    file.delete()

    return 1
    
@app.task
def ampq_deleteFile(gitlabId=None, file=None, message=None, branch="master"):
    
    git = gitlab.Gitlab(settings.GITLAB_URL, settings.GITLAB_TOKEN)

    git.createfile(gitlabId, file.file.name, branch, file.file.read(), message)
    
    return 1
    
@app.task
def ampq_createBranch(gitlabId=None, branch="master"):
    
    git = gitlab.Gitlab(settings.GITLAB_URL, settings.GITLAB_TOKEN)

    git.createbranch(gitlabId, branch, "master")
    
    return 1
    
@app.task
def ampq_downloadRepository(gitlabId=None, user=None):
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    temporary_folder = str(tempfile.mkdtemp())
    
    git = gitlab.Gitlab(settings.GITLAB_URL, settings.GITLAB_TOKEN)
    content = git.getfilearchive(gitlabId, filepath=temporary_folder+'/archive.tar.gz')
    
    fichier = open(temporary_folder+'/archive.tar.gz', "rb")
    content = ContentFile(base64.b64decode(fichier.read()))
    fichier.close()
 

    temp = DownloadUser()
    temp.user = user
    temp.name = 'archive.tar.gz'
    temp.file.save('archive.tar.gz', content)
    temp.save()
    

    # envoi de email
    #send_mail('Votre fichier est prêt - la maison des partitions', 'Votre fichier est prêt. Vous pouvez le télécharger en cliquant sur le lien suivant <a>Lien</a>', 'banco29510@gmail.com', ['antoine.hemedy@gmail.com'], fail_silently=False)

    return temp
    
@app.task
def ampq_downloadCommit(gitlabId=None, user=None, commit=None):
    
    temporary_folder = str(tempfile.mkdtemp())
    
    git = gitlab.Gitlab(settings.GITLAB_URL, settings.GITLAB_TOKEN)
    commit = git.getrepositorycommit(gitlabId, commit.hashCommit)
    commit = Commit.objects.get(hashCommit=commit['id'])
    
    files = git.getrepositorytree(gitlabId, path='', ref_name=commit.branch.name)
        
    for file in files:
        print(file)
        print(file['name'])
        raw = git.getrawfile(gitlabId, commit.hashCommit, filepath=file['name'])
        print(raw)
        
        if raw:
            fichier = open(temporary_folder+'/'+file['name'], "wb")
            fichier.write(raw)
            fichier.close()
        print(os.listdir(temporary_folder))
 
    # mise en zip
    print(make_archive(temporary_folder+'/archive', 'zip', temporary_folder))
    print(os.listdir(temporary_folder))
    
    fichier = open(temporary_folder+'/archive.zip', "rb")
    content = ContentFile(fichier.read())
    fichier.close()
    
    temp = DownloadUser()
    temp.user = user
    temp.name = 'archive.zip'
    temp.file.save('archive.zip', content)
    temp.save()

    # envoi de email
    #send_mail('Votre fichier est prêt - la maison des partitions', 'Votre fichier est prêt. Vous pouvez le télécharger en cliquant sur le lien suivant <a>Lien</a>', 'banco29510@gmail.com', ['antoine.hemedy@gmail.com'], fail_silently=False)

    return temp
    
@app.task
def ampq_downloadFile(gitlabId=None, file=None, user=None):

    git = gitlab.Gitlab(settings.GITLAB_URL, settings.GITLAB_TOKEN)
    
    raw = git.getrawfile(gitlabId, file.commit.hashCommit, filepath='readme.md')
    
    print(file.hashFile)
    print(raw)
    
    temp = DownloadUser()
    temp.name = file.name
    temp.user = user
    temp.file.save(file.name, ContentFile(raw), save=True)
    temp.save()

    # envoi de email
    #send_mail('Votre fichier est prêt - la maison des partitions', 'Votre fichier est prêt. Vous pouvez le télécharger en cliquant sur le lien suivant <a>Lien</a>', 'banco29510@gmail.com', ['antoine.hemedy@gmail.com'], fail_silently=False)

    return temp

@app.task
def ampq_updateDatabase(gitlabId=None):
    
    git = gitlab.Gitlab(settings.GITLAB_URL, settings.GITLAB_TOKEN)
    repository = get_object_or_404(Repository, gitlabId=gitlabId)
    
    
    branches = git.getbranches(gitlabId)
    print('branches : '+str(branches))
    
    for branch in branches:
        branch = branch['name']
        
        #try:
        #    print('try')
        #    branche = Branche.objects.get(name__exact=branch, repository=repository)
        #    print(branche)
        #except ObjectDoesNotExist:
        #    Branche(str(branch), repository).save()
        #    print('create')
        
        print(branch)
    
        commits = git.getrepositorycommits(gitlabId,)
        print('------------------------')
        
        print('commits : '+str(commits))
        
        for commit_gitlab in commits:
            
            if len(Commit.objects.filter(hashCommit=commit_gitlab['id'])) == 0: # si le commit n'existe pas
                commit = Commit()
                commit.repository = get_object_or_404(Repository, gitlabId=gitlabId)
                commit.hashCommit = commit_gitlab['id']
                commit.message = commit_gitlab['message']
                commit.date = commit_gitlab['created_at']
                commit.branch = branch
                commit.save()
    
                files = git.getrepositorytree(gitlabId, path='/', ref_name=branch)
        
                for file in files:
                    if len(File.objects.filter(hashFile=file['id'], commit=commit)) == 0: # si le fichier n'existe pas
                        file = File(hashFile=file['id'], name=file['name'], size=0)
                        file.commit = Commit.objects.get(hashCommit=commit_gitlab['id']) # ajout du commit
                        file.save()
    

    return 1

