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

import os, sys, glob, mimetypes, re, logging, pickle, tempfile, time, subprocess, json, base64, pprint
from datetime import datetime
from subprocess import *
from shutil import *

from djcelery import celery
from score.celery import *
from celery import Task
import gitlab

from repository.models import *

from git import Repo


@app.task
def ampq_addFile(gitlabId=None, file=None, message=None, branch="master"):
    
    # clone du dépot
    #cloned_repo = Repo.clone_from('https://banco29510:antoine29510@bitbucket.org/banco29510/score_c9.git', temp, branch='master')
    
    git = gitlab.Gitlab(settings.GITLAB_URL, settings.GITLAB_TOKEN)
        
    git.createfile(gitlabId, os.path.basename(file.file.name), branch, file.file.read(), message)
    #pprint.pprint(file)
    
    file.file.delete()
    file.delete()

    return 1
    
@app.task
def ampq_deleteFile(gitlabId=None, file=None, message=None, branch="master"):
    
    git = gitlab.Gitlab(settings.GITLAB_URL, settings.GITLAB_TOKEN)

    git.deletefile(gitlabId, file.file.name, branch,  message)
    
    return 1
    
@app.task
def ampq_renameFile(gitlabId=None, oldFile=None, newFile=None):
    
    git = gitlab.Gitlab(settings.GITLAB_URL, settings.GITLAB_TOKEN)

    # recuperation et stockage fichier
    raw = git.getrawfile(gitlabId, oldFile.commit.hashCommit, filepath=oldFile.name)

    #supression du fichier
    git.deletefile(gitlabId, oldFile.name, oldFile.commit.branch,  "Supresion du fichier "+oldFile.name)
    
    # ajout du fichier
    git.createfile(gitlabId, oldFile.name, oldFile.commit.branch, raw, 'Ajout du fichier '+newFile.name)
    
    
    return 1
    
@app.task
def ampq_createBranch(gitlabId=None, branch="master", parent_branch='master'):
    
    git = gitlab.Gitlab(settings.GITLAB_URL, settings.GITLAB_TOKEN)

    git.createbranch(gitlabId, branch, parent_branch)
    
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
def ampq_tagCommit(gitlabId=None, commit=None, tag_name=None):

    git = gitlab.Gitlab(settings.GITLAB_URL, settings.GITLAB_TOKEN)
    
    git.createrepositorytag(gitlabId, tag_name, commit.hashCommit, message='Ajout du tag '+tag_name)
    
    Tag(name=str(tag_name), commit=commit).save()

    # envoi de email
    #send_mail('Votre fichier est prêt - la maison des partitions', 'Votre fichier est prêt. Vous pouvez le télécharger en cliquant sur le lien suivant <a>Lien</a>', 'banco29510@gmail.com', ['antoine.hemedy@gmail.com'], fail_silently=False)

    return 1

@app.task
def ampq_mergeBranch(gitlabId=None, source_branch=None, target_branch='master'):

    git = gitlab.Gitlab(settings.GITLAB_URL, settings.GITLAB_TOKEN)
    
    merge = git.createmergerequest(gitlabId, source_branch, target_branch, 'Fusion de '+source_branch+' et de '+target_branch+'', )

    return 1

@app.task
def ampq_updateDatabase(pk=None):
    
    repository = get_object_or_404(Repository, pk=pk)
    temp = tempfile.mkdtemp()
    
    # clone du dépot
    cloned_repo = Repo.clone_from('https://banco29510:antoine29510@bitbucket.org/banco29510/score_c9.git', temp, branch='master')
    
    # list des branches
    branches = cloned_repo.heads
    for branch in branches:
        print(branch)
        if not Branche.objects.filter(name=str(branch), repository=repository).exists():
            Branche(name=branch, repository=repository).save()
    
    # liste des commits
    for commit in cloned_repo.iter_commits():
        if not Commit.objects.filter(hash=str(commit.binsha)).exists():
            commitDatabase = Commit(repository=repository, message=commit.message, hash=str(commit.binsha), date=datetime.now(),).save()
            
        print(commit.tree.trees)
        commitDatabase = Commit.objects.get(repository=repository, hash=str(commit.binsha))
        for tree in commit.tree.trees:
            if not File.objects.filter(hash=str(tree.binsha)).exists():
                treeDatabase = File(hash=str(tree.binsha), commit=commitDatabase, name=tree.name).save()
    
    return 1


