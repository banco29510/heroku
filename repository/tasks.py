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

import os, sys, datetime, glob, shutil, mimetypes, re, logging, pickle, tempfile, time, subprocess, json, base64, pprint

from djcelery import celery
from score.celery import *
from celery import Task

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
    author = pygit2.Signature('admin', 'admin@admin.fr')
    commiteur = pygit2.Signature('admin', 'admin@admin.fr')
    credential = pygit2.UserPass("anonymous", "anonymous")
    temporary_folder = tempfile.TemporaryDirectory()
    repository = ""
    index = ""


    def __init__(self, username=None, password=None, url=None, bare=False,):
        self.username = username
        self.password = password
        self.url = url
        self.bare = bare
        self.credential = pygit2.UserPass(username, password)

    ## ajout d'un fichier
    def add(self, file=None):
        print(file)
        #self.index = self.repository.index
        #self.index.add_all()
        #self.index.write()
        #tree = self.index.write_tree()
        
        return 1
        
        
    def clone(self):
        self.repository = pygit2.clone_repository(self.url, self.temporary_folder, bare=self.bare,)
        return 1

    def push(self):
        print('aaaaa')

    def commit(self):
        pass

    def listAllBranch(self):
        #self.local_branches = self.repository.listall_branches(pygit2.GIT_BRANCH_REMOTE)
        return self.local_branches

    def changeBranch(self):
        #self.repository.lookup_branch('master')

        return 1

    def checkout(self, hash='HEAD'):
        #self.repository.checkout(hash)
        return 1

    def commit(self):
        #oid = repository.create_commit('refs/heads/master',, self.author, self.commiter, "ajout du fichier",tree,[repo.head.get_object().hex])
        return 1

    def delete(self, path=None):
        #self.index.remove(path)
        #self.index.write()
        #tree = self.index.write_tree()
		
        return 1


    def listFiles(self):
        #self.files = self.index
        return self.index


    def listCommits(self):
        #for commit in self.repository.walk(self.repository.head.target, pygit2.GIT_SORT_TOPOLOGICAL):
            #self.commits.append(commit)
        return 1


@app.task
def ampq_addFile(username=None, password=None, url=None, file=None):
    
    git = GitMethods(username=username, password=password, url=url)
    git.clone()
    #git.add(file)
    #git.commit()
    #git.push()
    # updateDatabase()
    #print(git.listAllBranch())

    return 1
    
@app.task
def ampq_deleteFile(username=None, password=None, url=None,):
    
    git = GitMethods(username=username, password=password, url=url,)
    git.clone()
    #git.add()
    #print(git.listAllBranch())

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
    #cred = pygit2.UserPass(username, password)
    #repo = pygit2.clone_repository(url, temporary_folder, bare=bare, credentials=cred)

    return temporary_folder

@app.task
def addFile(username=None, password=None, url=None, file=None):
    temporary_folder = downloadRepository(username=username, password=password, url=url)
    reference = 'refs/heads/master'

    with open(temporary_folder+'/'+file.name, 'wb+') as file_media:
            file_media.write(file.read())

    index = repo.index
    index.add_all()
    index.write()
    author = pygit2.Signature('admin', 'admin@admin.fr')
    commiter = pygit2.Signature('admin', 'admin@admin.fr')
    tree = index.write_tree()
    oid = repo.create_commit(reference, author, commiter, message,tree,[repo.head.get_object().hex])


    all_refs = repo.listall_references()

    remote = repo.remotes[0]
    remote.credentials = pygit2.UserPass(username, password)
    remote.add_push('refs/heads/master')

    #remote.push_url = 'https://git@gitlab.com/banco29510/rrrr.git' # avec authentification
    remote.push_url = 'https://banco29510%40gmail.com:antoine29510@gitlab.com/banco29510/rrrr.git' # sans authentification
    signature = pygit2.Signature('banco29510@gmail.com', 'antoine29510')

    #remote.push(all_refs[1], signature, message)
    remote.push_refspecs
    remote.push(reference) # remote.push(reference, signature=signature) fonctionne avec la nouvelle version

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