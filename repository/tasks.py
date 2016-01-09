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
from django.views.generic.edit import *
from django.conf import settings

import os, sys, datetime, glob, shutil, mimetypes, re, logging, pickle, tempfile, time, subprocess, json, base64, pprint

from djcelery import celery
from score.celery import *
from celery import Task
import gitlab

from repository.models import *

import pygit2 as pygit2

class GitMethods():
    local_branches = []
    commits = []
    files = []
    username = ""
    password = ""
    url = ""
    bare = False
    temporary_folder = tempfile.TemporaryDirectory()
    repository = ""
    index = ""
    git = ""
    gitlabId = 0


    def __init__(self, gitlabId=None):
        self.git = gitlab.Gitlab(settings.GITLAB_URL, settings.GITLAB_TOKEN)
        self.gitlabId = gitlabId

    ## ajout d'un fichier
    def add(self, file=None):
        
        #self.git.createfile(gitlabId, file_path, "master", content, "message")
        pprint.pprint(file)
        
        return 1
        

@app.task
def ampq_addFile(gitlabId=None, file=None):
    
    git = gitlab.Gitlab(settings.GITLAB_URL, settings.GITLAB_TOKEN)
        
    git.createfile(gitlabId, file.file.name, "master", file.file.read(), "Ajout du readme")
    #pprint.pprint(file)
    
    git.createbranch(gitlabId, "dev", "master")
    
    file.file.delete()
    file.delete()
    
    return 1
    
    
@app.task
def ampq_updateDatabase(gitlabId=None):
    
    git = gitlab.Gitlab(settings.GITLAB_URL, settings.GITLAB_TOKEN)
    branches = git.getbranches(gitlabId)
    
    for branch in branches:
        branch = branch['name']
    
        commits = git.getrepositorycommits(gitlabId,)
    
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
            if len(File.objects.filter(hashFile=file['id'])) == 0: # si le fichier n'existe pas
                file = File(hashFile=file['id'], name=file['name'], size=0)
                file.commit = Commit.objects.get(hashCommit=commit_gitlab['id']) # ajout du commit
                file.save()
    
    return 1    
    
@app.task
def ampq_deleteFile(file=None):

    return 1

@app.task
def ampq_downloadRepository(username=None, password=None, url=None,):

    #git = GitMethods(username=username, password=password, url=url,)
    #git.clone()
    #shutil.make_archive(git.temporary_folder+'/'+'archive', 'zip', git.temporary_folder) # créer le zip ou le tar

    #print(git.temporary_folder+'/'+'archive')
    #print(base64.b64decode(open(git.temporary_folder+'/'+'archive.zip').read()))
    temp = TemporaryFile()
    temp.name = 'archive.zip'
    temp.file.save('archive.zip', ContentFile(base64.b64encode(open(git.temporary_folder+'/'+'archive.zip'))))
    temp.save()

    # envoi de email
    #send_mail('Votre fichier est prêt - la maison des partitions', 'Votre fichier est prêt. Vous pouvez le télécharger en cliquant sur le lien suivant <a>Lien</a>', 'banco29510@gmail.com', ['antoine.hemedy@gmail.com'], fail_silently=False)

    return temp

@app.task
def downloadRepository(username=None, password=None, url=None, bare=False):
    temporary_folder = tempfile.mkdtemp()
    print(temporary_folder)
    return temporary_folder

@app.task
def addFile(username=None, password=None, url=None, file=None):
    temporary_folder = downloadRepository(username=username, password=password, url=url)
    reference = 'refs/heads/master'
    
    with open(temporary_folder+'/'+file.name, 'wb+') as file_media:
            file_media.write(file.read())
            
    updateDatabase.delay(username=username, password=password, url=url)
    return 1

@app.task
def renameFile(username=None, password=None, url=None, file=None):
    return 1

@app.task
def replaceFile(file=None):
    return 1

@app.task
def listCommit(temp=None):
    return 1

@app.task
def listFile(temp=None):
    return 1

@app.task
def updateDatabase(username=None, password=None, url=None):

    temporary_folder = tempfile.mkdtemp()
    cred = pygit2.UserPass('banco29510@gmail.com', 'antoine29510')
    repo = pygit2.clone_repository('https://banco29510%40gmail.com:antoine29510@gitlab.com/banco29510/rrrr.git', temporary_folder, bare=False, credentials=cred)

    all_refs = repo.listall_references()
    print(all_refs)

    for branch in repo.listall_branches():
        print(branch)

        # change de branche
        branch = repo.lookup_branch(branch)
        ref = repo.lookup_reference(branch.name)
        repo.checkout(ref)

        for remoteCommit in repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL):
            print(remoteCommit.id)
            if len(Commit.objects.filter(hashCommit=remoteCommit.id, branch=branch.name)) == 0: # si le commit n'existe pas
                commit = Commit()
                commit.repository = get_object_or_404(Repository, url='https://gitlab.com/banco29510/rrrr.git')
                commit.hashCommit = remoteCommit.id
                commit.message = remoteCommit.message
                commit.date = datetime.datetime.utcfromtimestamp(remoteCommit.commit_time)
                commit.branch = branch.name
                commit.save()

                for entry in remoteCommit.tree:
                    print(entry.id, entry.name)
                    if len(File.objects.filter(hashFile=entry.id)) == 0: # si le fichier n'existe pas
                        file = File(hashFile=entry.id, name=entry.name, size=os.path.getsize(temporary_folder+'/'+entry.name)).save()

                        dataFile = File.objects.get(hashFile=entry.id)
                        dataFile.commits.add(commit) # ajout du commit


    for commit in repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL):
        print(commit.message)


    return repo