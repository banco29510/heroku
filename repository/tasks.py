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

import os, sys, glob, mimetypes, re, logging, pickle, tempfile, time, subprocess, json, base64, pprint, hashlib, shutil, binascii
from datetime import datetime
from subprocess import *
from shutil import *

from djcelery import celery
from score.celery import *
from celery import Task
import gitlab

from repository.models import *

from git import Repo, Actor, Head, Remote, Git, Blob, Tree


## \brief créer le dépot en ajoutant les fichiers
@app.task
def ampq_createRepository(id=None):
    
    repository = get_object_or_404(Repository, pk=id)
    temp = tempfile.mkdtemp()
    
    # création du dépot du dépot
    repo = Repo.init(temp+'/')
    remote = repo.create_remote('origin', repository.url)
    
    new_file_path = os.path.join(repo.working_tree_dir, 'readme.md')
    fichier = open(new_file_path, 'w')
    fichier.write('### Partition ' + repository.name)
    fichier.close()                            
    repo.index.add([new_file_path]) 
    
    new_file_path = os.path.join(repo.working_tree_dir, 'licence.txt')
    fichier = open(new_file_path, 'w')
    fichier.write('Licence libre')
    fichier.close()        
    repo.index.add([new_file_path]) 
    
    author = Actor("An author", "author@example.com")
    committer = Actor("A committer", "committer@example.com")
    
    repo.index.commit("initial commit", author=author, committer=committer)
    
    print(os.listdir(temp))
    
    # création de la branche dev
    repo.git.checkout('HEAD', b="dev")
    remote.push()
    
    #changement pour la branche master
    repo.git.checkout('master')
    remote.push()
    
    #push des branches
    for head in repo.heads:
        print(head)
        
    return 1
    
@app.task
def ampq_addFile(id=None, file=None, message=None, branch="master"):
    
    repository = get_object_or_404(Repository, pk=id)
    temp = tempfile.mkdtemp()
    
    repo = Repo.clone_from(repository.url, temp, branch=branch) # clone du dépot
    
    new_file_path = os.path.join(repo.working_tree_dir, os.path.basename(file.file.name))
    fichier = open(new_file_path, 'wb')
    fichier.write(file.file.read())
    fichier.close()                            
    repo.index.add([new_file_path]) 
    
    print(temp+'/'+file.file.name+'/')
    print(os.path.basename(file.file.name))
    print(temp+'/'+os.path.basename(file.file.name))
    
    author = Actor("Utilisateur", "mail@gmail.com")
    committer = Actor("admin la maison des partitions", "lamaisondespartitions@gmail.com")
        
    repo.index.commit(message, author=author, committer=committer)
    
    repo.remotes.origin.push()
        
    file.file.delete()
    file.delete()

    return 1
    
@app.task
def ampq_deleteFile(id=None, file=None, message=None, branch="master"):
    
    repository = get_object_or_404(Repository, pk=id)
    temp = tempfile.mkdtemp()
    
    # clone du dépot
    repo = Repo.clone_from(repository.url, temp, branch=branch) # clone du dépot
    
    #repo.git.checkout(branch)
    
    new_file_path = os.path.join(repo.working_tree_dir, os.path.basename(file.name))                           
    repo.index.remove([new_file_path]) 
    
    print(temp+'/'+file.name+'/')
    print(os.path.basename(file.name))
    print(temp+'/'+os.path.basename(file.name))
    
    author = Actor("Utilisateur", "mail@gmail.com")
    committer = Actor("admin la maison des partitions", "lamaisondespartitions@gmail.com")
        
    repo.index.commit(str(message), author=author, committer=committer)
    
    repo.remotes.origin.push()
    
    
    return 1
    
@app.task
def ampq_renameFile(id=None, file=None, newNameFile=None):
    
    repository = get_object_or_404(Repository, pk=id)
    temp = tempfile.mkdtemp()
    
    # clone du dépot
    repo = Repo.clone_from(repository.url, temp, branch=file.commit.branch.name)
    
    print(repo.working_tree_dir)
    print(file.name)
    print(str(file.extension()))
    
    # recuperation du contenu
    fichier = open(repo.working_tree_dir+'/'+file.name, 'rb')
    content = fichier.read()
    fichier.close()
    
    new_file_path = os.path.join(repo.working_tree_dir, os.path.basename(file.name))                      
    repo.index.remove([new_file_path]) # suprimme le fichier
    
    new_file_path = os.path.join(repo.working_tree_dir, newNameFile+str(file.extension()))
    fichier = open(new_file_path, 'wb')
    fichier.write(content)
    fichier.close()                            
    repo.index.add([new_file_path])  # remet le fichier avec un nouveau nom
    
    author = Actor("Utilisateur", "mail@gmail.com")
    committer = Actor("admin la maison des partitions", "lamaisondespartitions@gmail.com")
        
    repo.index.commit('Renommage du fichier '+ file.name+' en '+newNameFile , author=author, committer=committer)
    
    repo.remotes.origin.push()
    
    return 1
    
@app.task
def ampq_createBranch(id=None, branch="master", parent_branch='master'):
    
    repository = get_object_or_404(Repository, pk=id)
    temp = tempfile.mkdtemp()
    
    # clone du dépot
    repo = Repo.clone_from(repository.url, temp)
    
    repo.git.checkout('HEAD', b=branch)   
    
    repo.remotes.origin.push()
    
    return 1
    
## \brief Prépare une archive avec l'ensemble des fichiers d'un dépot
#
@app.task
def ampq_downloadRepository(id=None, user=None):
    
    repository = get_object_or_404(Repository, pk=id)
    temp = tempfile.mkdtemp()
    temp_archive = tempfile.mkdtemp()
    
    repo = Repo.clone_from(repository.url, temp, ) # clone du dépot
    
    shutil.make_archive(temp_archive+'/archive', 'zip', temp)
    
    fichier = open(temp_archive+'/archive.zip', "rb")
    content = ContentFile(fichier.read())
    fichier.close()

    temp = DownloadUser()
    temp.user = user
    temp.name = 'archive.zip'
    temp.file.save('archive.zip', content)
    temp.save()
    
    # envoi de email
    #send_mail('Votre fichier est prêt - la maison des partitions', 'Votre fichier est prêt. Vous pouvez le télécharger en cliquant sur le lien suivant <a>Lien</a>', 'banco29510@gmail.com', ['antoine.hemedy@gmail.com'], fail_silently=False)

    return 1
    
@app.task
def ampq_downloadCommit(id=None, user=None, commit=None):
    
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
def ampq_downloadFile(id=None, file=None, user=None):

    repository = get_object_or_404(Repository, pk=id)
    temp = tempfile.mkdtemp()
    
    repo = Repo.clone_from(repository.url, temp, branch=file.commit.branch.name) # clone du dépot
    
    repo.git.checkout(file.commit.hash)
    
    fichier = open(temp+'/'+file.name, "rb")
    content = ContentFile(fichier.read())
    fichier.close()

    
    temp = DownloadUser()
    temp.name = file.name
    temp.user = user
    temp.file.save(file.name, content, save=True)
    temp.save()

    # envoi de email
    #send_mail('Votre fichier est prêt - la maison des partitions', 'Votre fichier est prêt. Vous pouvez le télécharger en cliquant sur le lien suivant <a>Lien</a>', 'banco29510@gmail.com', ['antoine.hemedy@gmail.com'], fail_silently=False)

    return temp
    
@app.task
def ampq_tagCommit(id=None, commit=None, tag_name=None):
    
    repository = get_object_or_404(Repository, pk=id)
    commit = get_object_or_404(Commit, pk=commit)
    temp = tempfile.mkdtemp()
    
    repo = Repo.clone_from(repository.url, temp, branch=commit.branch.name) # clone du dépot
    
    past = cloned_repo.create_tag('past', ref=repo.heads.master,  message="This is a tag-object pointing to ")
    
    repo.remotes.origin.push()
    

    # envoi de email
    #send_mail('Votre fichier est prêt - la maison des partitions', 'Votre fichier est prêt. Vous pouvez le télécharger en cliquant sur le lien suivant <a>Lien</a>', 'banco29510@gmail.com', ['antoine.hemedy@gmail.com'], fail_silently=False)

    return 1

@app.task
def ampq_mergeBranch(id=None, source_branch=None, target_branch='master'):

    repository = get_object_or_404(Repository, pk=id)
    
    temp = tempfile.mkdtemp()
    
    repo = Repo.clone_from(repository.url, temp, branch=source_branch) # clone du dépot

    repo.git.checkout(source_branch)
    
    repo.merge_base(target_branch, source_branch)
    
    #repo.index.merge_tree(source_branch, base=target_branch)  


    return 1

## \brief remplit la BDD à partir du dépot
@app.task
def ampq_updateDatabase(pk=None):
    
    repository = get_object_or_404(Repository, pk=pk)
    softwares = get_list_or_404(Software)
    licences = get_list_or_404(Licence)
    temp = tempfile.mkdtemp()
    
    # clone du dépot
    cloned_repo = Repo.clone_from(repository.url, temp)
    
    # list des branches
    #print(cloned_repo.heads)
    #for head in cloned_repo.heads:
    #    print('head '+ str(head))
    #print(cloned_repo.refs)
    
    # liste les branches du dépot et réalise un checkout
    for ref in cloned_repo.refs:
        #print(ref.name)
        if not ref.name.find("origin"):
            if ref.name.replace('origin/','') != 'HEAD':
                cloned_repo.git.checkout(ref.name.replace('origin/',''))
        
    #print(cloned_repo.remotes)
    #for remote in cloned_repo.remotes:
    #    print('remote '+str(remote))
    
    #cloned_repo.git.checkout('master')
    #pprint.pprint(cloned_repo.heads)
    
    
    for branch in cloned_repo.heads:
        #print('branche : '+str(branch))
        cloned_repo.git.checkout(branch)
        
        if not Branche.objects.filter(name=str(branch), repository=repository).exists():
            Branche(name=branch, repository=repository).save()
            branchDatabase = Branche.objects.get(name=str(branch), repository=repository)
        else:
            branchDatabase = Branche.objects.get(name=str(branch), repository=repository)
     
     
        # liste des commits
        for commit in cloned_repo.iter_commits():
            #print(str(commit.hexsha)+'***'+str(commit.tree)+'***'+str(commit.binsha))
            #print(str(hashlib.sha256(commit.tree.binsha).hexdigest()))
            #print(str(commit.binsha.decode('utf8', 'ignore')))
            #print(commit.hexsha)
            #print(binascii.hexlify(commit.binsha).decode('utf-8'))

            if not Commit.objects.filter(hash=binascii.hexlify(commit.binsha).decode('utf-8'), repository=repository, branch=branchDatabase).exists():
                commitDatabase = Commit(repository=repository, message=commit.message, hash=binascii.hexlify(commit.binsha).decode('utf-8'), date=datetime.now(), branch=branchDatabase, size=10).save()
            else:
                cloned_repo.git.checkout(binascii.hexlify(commit.binsha).decode('utf-8'))
                
                
            #pprint.pprint(commit)  
            #pprint.pprint(commit.tree)  
            #pprint.pprint(commit.tree.trees)
            #for entry in commit.tree:                                         
            #    print(entry.name)
            commitDatabase = Commit.objects.get(repository=repository, branch=branchDatabase, hash=binascii.hexlify(commit.binsha).decode('utf-8'))
            
            
            # ajoute les auteurs
            
            #print(commit.author.name)
            #print(commit.author.email)
            #if not 
            author_commit = Author(commit=commitDatabase, name=str(commit.author.name), email=str(commit.author.email)).save()
            #else:
            #
            
            for tree in commit.tree:
                #print('fichier :'+str(tree.name))
                #print(str(tree.binsha) + str(tree.name) + str(hashlib.sha256(tree.name.encode('utf8')).hexdigest()))
                #print(hashlib.sha256(tree.name.encode('utf8')).hexdigest())
                #print(cloned_repo.working_tree_dir)
                if not File.objects.filter(hash=str(hashlib.sha256(tree.name.encode('utf8')).hexdigest()), commit=commitDatabase).exists():
                    treeDatabase = File(hash=str(hashlib.sha256(tree.name.encode('utf8')).hexdigest()), commit=commitDatabase, name=tree.name, size=os.path.getsize(cloned_repo.working_tree_dir+'/'+tree.name),).save()
                
                
                fileDatabase = File.objects.filter(hash=str(hashlib.sha256(tree.name.encode('utf8')).hexdigest()), commit=commitDatabase)
                repo_size = 0
                for fileDatabase in fileDatabase:
                    #print(fileDatabase)
                    for software in softwares:
                        if fileDatabase.extension() == software.extension:
                            fileDatabase.software = software
                            
                    for licence in licences:
                            if licence.name == 'Copyright':
                                fileDatabase.licence = licence
                                
                    repo_size = int(repo_size) + int(fileDatabase.size)
                            
                    fileDatabase.save()
                    
                repository.size = repo_size # ajoute la taille du dépot   
                
                
    
    return 1

@app.task
def ampq_replaceFile(id=None, file=None, replacefile=None):
    
    repository = get_object_or_404(Repository, pk=id)
    temp = tempfile.mkdtemp()
    
    # clone du dépot
    repo = Repo.clone_from(repository.url, temp, branch=file.commit.branch.name)
    
    # recuperation du contenu
    fichier = open(repo.working_tree_dir+'/'+file.name, 'rb')
    content = fichier.read()
    fichier.close()
    
    new_file_path = os.path.join(repo.working_tree_dir, os.path.basename(file.name))                      
    repo.index.remove([new_file_path]) # suprimme le fichier
    
    new_file_path = os.path.join(repo.working_tree_dir, replaceFile+str(file.extension()))
    fichier = open(new_file_path, 'wb')
    fichier.write(content)
    fichier.close()                            
    repo.index.add([new_file_path])  # remet le fichier avec un nouveau nom
    
    author = Actor("Utilisateur", "mail@gmail.com")
    committer = Actor("admin la maison des partitions", "lamaisondespartitions@gmail.com")
        
    repo.index.commit('Remplacement du fichier '+ file.name+' en '+replaceFile , author=author, committer=committer)
    
    repo.remotes.origin.push()
    
    return 1