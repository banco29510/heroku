# -*- coding: utf-8 -*-
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

import pprint, tempfile, os, sys, json, datetime, time, mimetypes, zipfile, shutil, base64

from gitlab import *
from celery import Celery
from celery import chain, group, chord
from .tasks import *


from repository.models import *
from repository.forms import *

from repository.tasks import *

## recherche des partitions
def search(request):

    if request.GET.get("name", None) != None:
        repositorys = Repository.objects.filter(name__contains=request.GET.get("name", None))
    else:
        repositorys = Repository.objects.all()

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            author = form.cleaned_data['author']
            instrument = form.cleaned_data['instrument']
            software = form.cleaned_data['software']


            if name:
                repositorys = Repository.objects.filter(name__icontains=name)
            else:
                repositorys = Repository.objects.all()

            if author:
                print('auteur')
                listAuthor = []

                for repository in repositorys:
                    if repository.scoreAuthor == author:
                        listAuthor.append(repository)

                repositorys = list(set(listAuthor))

            if instrument:
                print("instrument")

                # les instruments
                listInstrument = []
                for repository in repositorys:
                    commits = Commit.objects.filter(repository=repository)

                    for commit in commits:
                        files = File.objects.filter(commits__in=[commits]) # liste des fichiers dans le dépot
                        for file in files:
                            if instrument in file.instrument.all():
                                listInstrument.append(repository)

                repositorys = list(set(listInstrument))

            if software:
                print("logiciel")

                # les logiciels
                listSoftware= []
                for repository in repositorys:
                    commits = Commit.objects.filter(repository=repository)

                    for commit in commits:
                        files = File.objects.filter(commit__in=[commits]) # liste des fichiers dans le dépot
                        for file in files:
                            if file.software in software:
                                listSoftware.append(repository)

                repositorys = list(set(listSoftware))


    else:
        form = SearchForm(initial={'name': request.GET.get("name", None)})

    paginator = Paginator(repositorys, 20)

    page = request.GET.get('page', 1)
    try:
        repositorys = paginator.page(page)
    except PageNotAnInteger:
        repositorys = paginator.page(1)
    except EmptyPage:
        repositorys = paginator.page(paginator.num_pages)

    return render(request, 'repository/search.html', {'repositorys': repositorys, 'form': form,})

## créer une partition
@login_required
def newScore(request):
    
    if request.method == 'POST':
        form = NewRepositoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name'].replace(' ', '-')
            scoreAuthor = form.cleaned_data['scoreAuthor']

            gitlab = Gitlab(settings.GITLAB_URL, settings.GITLAB_TOKEN)
            
            gitlab.createproject(name) # creation projet
           
            projects = gitlab.getprojectsowned()
            for project in projects:
                #print(project['name'].lower()+'=='+name.lower())
                if project['name'].lower() == name.lower():
                    gitlabId = project['id']
            
            # création du dépot dans la bdd
            repository = Repository()
            repository.name = name
            repository.scoreAuthor = scoreAuthor
            repository.gitlabId = gitlabId
            repository.save()
            
            # mise a jour du dépot
            temporary_folder = tempfile.mkdtemp()
            TempFile = TemporaryFile()
            TempFile.name = "readme.md"
            TempFile.file.name = "readme.md"
            TempFile.file.save("readme.md", ContentFile("Partition "+repository.name+""), save=True)
                
            TempFile.save() 
            
            #ampq_addFile.apply_async((gitlabId, TempFile, "Ajout du readme", "master"), link=ampq_updateDatabase.s(gitlabId))()
            
            #ampq_addFile.s(gitlabId=gitlabId, file=TempFile, message="Ajout du readme", branch="master") | ampq_updateDatabase.s(gitlabId=gitlabId,) 
            #(ampq_addFile.s(gitlabId, TempFile, "Ajout du readme", "master") | ampq_updateDatabase.subtask(gitlabId) ).apply_async()
            #ampq_addFile.delay(gitlabId, TempFile, "Ajout du readme", "master") | ampq_updateDatabase.delay(gitlabId) 
            #chain(ampq_addFile.s(gitlabId, TempFile, "Ajout du readme", "master"), ampq_updateDatabase.s(args=gitlabId))()
            
            ampq_addFile.delay(gitlabId=gitlabId, file=TempFile, message="Ajout du readme", branch="master") # ajout readme.md
            ampq_createBranch.delay(gitlabId=gitlabId, branch="dev") # creation branche dev
            ampq_updateDatabase.delay(gitlabId) # update database

            
            messages.add_message(request, messages.INFO, 'Le dépot à été crée. Première révision lors de la prochaine mise à jour.')
            return redirect('repository-search',)

    else:
        form = NewRepositoryForm(initial={})


    return render(request, 'repository/newScore.html', {'form': form,})

## ajoute un fichier
@login_required
def addFile(request, pk=None):

    repository = get_object_or_404(Repository, pk=pk)
    
    try:
        commits = get_list_or_404(Commit, repository=repository.id)
    except:
        commits = []
    

    # liste des branches
    branches = []
    for commit in commits:
        if not commit.branch in branches:
            branches.append(commit.branch)
    
    list_branch = []
    for branch in branches:
        list_branch.append((branch, branch.capitalize()))
        
    branches = list_branch # met la liste des branches dans la variable branches
  
    if request.method == 'POST':
        form = AddFileForm(request.POST, request.FILES)
        form.fields['branch'].choices = branches

        if form.is_valid():
           
            message = form.cleaned_data['comment']
            file = request.FILES['file']
            branch = form.cleaned_data['branch']
            
            
            # mise a jour du dépot
            temporary_folder = tempfile.mkdtemp()
            TempFile = TemporaryFile()
            TempFile.name = file.name
            TempFile.file.name = file.name
            TempFile.file.save(file.name, ContentFile(file.read()), save=True)
                
            TempFile.save() 
            
            ampq_addFile.delay(gitlabId=repository.gitlabId, file=TempFile, message=message, branch=branch)
            ampq_updateDatabase.delay(gitlabId=repository.gitlabId) 
                
            messages.add_message(request, messages.INFO, 'Le fichier à été sauvegardé, la mise à jour sera effectué sous peu.')

            return redirect('repository-showRepositoryDeveloppement', pk=repository.id)


    else:

        form = AddFileForm(initial='',)
        form.fields['branch'].choices = branches



    return render(request, 'repository/addFile.html', {'form': form, 'repository': repository,})
    
## voir le depot en production avec juste la derniere version
@login_required
def showRepositoryProduction(request, pk=None):

    repository = get_object_or_404(Repository, pk=pk)
    commits = Commit.objects.filter(repository=repository).order_by('-date')
    try:
        commit = commits[0]
    except:
        commit = []
    try:
        files = File.objects.filter(commit = commits[0])
        readme = File.objects.get(commit = commits[0], name="readme.md")
    except:
        files = []
        readme = []
        
    print(readme)

    return render(request, 'repository/showRepositoryProduction.html', {'repository': repository, 'files': files, 'readme': readme, 'commit': commit,})

## Voir un fichier
def showFile(request, pk=None, pk_commit=None):

    file = get_object_or_404(File, pk=pk)
    commit = get_object_or_404(Commit, pk=pk_commit)
    repository = commit.repository

    return render(request, 'repository/showFile.html', {'file': file, 'commit': commit, 'extension': file.extension()})

##
# \brief Page download fichier pour afficher dans les templates
# \author A. H.
# \fn def downloadViewsFile(request, pk=None, pk_commit=None):
# \param[in] request requête Django
# \param[in] pk=None id du fichier
# \param[in] pk_commit=None id du commit
# \return response
#
@login_required
def downloadViewsFile(request, pk=None, pk_commit=None):

    file = get_object_or_404(File, pk=pk)
    commit = get_object_or_404(Commit, pk=pk_commit)
    repository = commit.repository

    git = gitlab.Gitlab(settings.GITLAB_URL, settings.GITLAB_TOKEN)
    file_64 = git.getfile(repository.gitlabId, file.name, commit.branch)
    content = str(file_64['content'])
    content = base64.b64decode(content)

    response = HttpResponse()

    response['Content-Type'] = mimetype=mimetypes.guess_type(str(file_64['file_name']))[0]
    response['Content-Disposition'] = 'inline; filename='+str(file_64['file_name'])
    response['Content-Length'] = str(file_64['size'])
    response.write(content)

    return response

##
# \brief Page download le dépot
# \author A. H.
# \fn def downloadRepository(request, commit=None):
# \param[in] commit=None id du commit
# \return le dossier zip du dépot
#
@login_required
def downloadCommit(request, pk=None):

    commit = get_object_or_404(Commit, pk=pk)
    repository = get_object_or_404(Repository, pk=commit.repository.id)
    temporary_folder = tempfile.mkdtemp()
    print(temporary_folder)
    cred = pygit2.UserPass('banco29510@gmail.com', 'antoine29510')
    repo = pygit2.clone_repository(repository.url, temporary_folder, bare=False, credentials=cred)


    response = HttpResponse()

    response['Content-Type'] = mimetype=mimetypes.guess_type(repository.name+'.zip')[0]
    response['Content-Disposition'] = 'attachment; filename='+repository.name+'.zip'
    response['Content-Length'] = os.path.getsize(temporary_folder+'/'+repository.name+'.zip')
    response.write(open(temporary_folder+'/'+repository.name+'.zip', 'rb').read())

    return response


## Voir la page du dépot en developpement
@login_required
def showRepositoryDeveloppement(request, pk=None):


    repository = get_object_or_404(Repository, pk=pk)
    commits = Commit.objects.filter(repository=repository).order_by('-date')
    try:
        commit = commits[0]
    except:
        commit = []
    try:
        files = File.objects.filter(commit = commits[0])
        readme = File.objects.get(commit = commits[0], name = "readme.md")
    except:
        files = []
        readme = []

    return render(request, 'repository/showRepositoryDeveloppement.html', {'repository': repository, 
                                                                            'files': files, 
                                                                            'commit': commit, 
                                                                            'readme': readme,
                                                                            'commits': commits,
                                                                            })


## renomme un fichier
@login_required
def renameFile(request, pk=None, pk_commit=None):

    file = get_object_or_404(File, pk=pk)
    commit = get_object_or_404(Commit, pk=pk_commit)

    temporary_folder = tempfile.mkdtemp()
    print(temporary_folder)

    #updateDatabase.delay(username='banco29510@gmail.com', password='antoine29510', url='https://banco29510%40gmail.com:antoine29510@gitlab.com/banco29510/rrrr.git')

    return render(request, 'repository/renameFile.html', {})

## suprimme un fichier
@login_required
def deleteFile(request, pk=None, pk_commit=None):

    file = get_object_or_404(File, pk=pk)
    commit = get_object_or_404(Commit, pk=pk_commit)
    
    if request.method == 'POST':
        form = DeleteFileForm(request.POST, request.FILES)
        

        if form.is_valid():
            
            ampq_deleteFile.delay(commit.repository.gitlabId, file, "supression fichier", file.commit.branch)
            ampq_updateDatabase.delay(gitlabId=commit.repository.gitlabId) 
                
            messages.add_message(request, messages.INFO, 'Le fichier à été suprimmé, la mise à jour sera effectué sous peu.')

            return redirect('repository-showRepositoryDeveloppement', pk=commit.repository.id)


    else:

        form = DeleteFileForm(initial='',)
        


    return render(request, 'repository/deleteFile.html', {'form': form, 'repository': commit.repository,})

## confirme le telechargement du fichier
@login_required
def warningDownloadFile(request, pk=None, pk_commit=None):

    file = get_object_or_404(File, pk=pk)
    commit = get_object_or_404(Commit, pk=pk_commit)

    ampq_downloadFile(commit.repository.gitlabId, file, request.user)
    

    return render(request, 'repository/warningDownloadFile.html', {})

## telechargement du fichier
@login_required
def downloadFile(request):
    return render(request, 'repository/deleteFile.html', {})

## confirme le telechargement du dépot
@login_required
def warningDownloadRepository(request, pk=None,):

    repository = get_object_or_404(Repository, pk=pk)

    ampq_downloadRepository.delay(username='banco29510@gmail.com', password='antoine29510', url='https://gitlab.com/banco29510/rrrr.git')

    # envoi du mail
    #ampq_sendMail.delay(user=request.user,)


    return render(request, 'repository/warningDownloadRepository.html', {})

## telechargement du dépot
@login_required
def downloadFile(request):
    return render(request, 'repository/deleteFile.html', {})

## confirme le telechargement du fichier
@login_required
def warningDownloadCommit(request, pk=None,):

    return render(request, 'repository/warningDownloadCommit.html', { })

## telechargement du fichier
@login_required
def downloadCommit(request):
    return render(request, 'repository/deleteFile.html', {})

##
@login_required
def listCommits(request, pk=None):

    repository = Repository.objects.get(pk=pk)
    try:
        commits = get_list_or_404(Commit, repository=repository)
    except:
        commits = []

    # liste des branches
    branches = []
    for commit in commits:
        if not commit.branch.split('/')[-1].capitalize() in branches:
            name = commit.branch.split('/')[-1].capitalize()
            branches.append(name)
    
    form = createBranchForm(initial='',)

    paginator = Paginator(commits, 20)

    page = request.GET.get('page', 1)
    try:
        commits = paginator.page(page)
    except PageNotAnInteger:
        commits = paginator.page(1)
    except EmptyPage:
        commits = paginator.page(paginator.num_pages)


    return render(request, 'repository/listCommits.html', {
        'repository': repository, 
        'commits': commits, 
        'branches': branches, 
        'form': form,
    })

##
@login_required
def listContributeurs(request, pk=None):

    repository = get_object_or_404(Repository, pk=pk)
    try:
        commits = get_list_or_404(Commit, repository=repository)
    except:
        commits = []

    authors = []
    for commit in commits:
        if not commit.author in authors and commit.author != None:
            authors.append(commit.author.capitalize())

    return render(request, 'repository/listContributeurs.html', {'repository': repository, 'authors': authors})

## demande de publication
@login_required
def publishDemand(request):
    return render(request, 'repository/publishDemand.html', {})

##
@login_required
def deleteCommit(request, pk=None):

    commit = get_object_or_404(Commit, pk=pk)

    temporary_folder = tempfile.mkdtemp()
    print(temporary_folder)
    
    messages.add_message(request, messages.INFO, 'L\' opération est en cours, le commit sera suprimme sous peu.')

    return render(request, 'repository/deleteCommit.html', {})

##
@login_required
def changeDeprecated(request, pk=None, boolean=True):

    commit = get_object_or_404(Commit, pk=pk)

    commit.deprecated = boolean
    commit.save()

    if commit.deprecated == True:
        messages.add_message(request, messages.INFO, 'Le dépot est déprécié.')
    else:
        messages.add_message(request, messages.INFO, 'Le dépot n\'est plus déprécié.')


    return render(request, 'repository/changeDeprecated.html', {})

##
@login_required
def restartRepositoryByOldCommit(request, pk=None):

    commit = get_object_or_404(Commit, pk=pk)

    temporary_folder = tempfile.mkdtemp()
    print(temporary_folder)
    
    return render(request, 'repository/restartRepositoryByOldCommit.html', {})

##
@login_required
def mergeCommit(request,):

    temporary_folder = tempfile.mkdtemp()
    print(temporary_folder)

    return render(request, 'repository/mergeCommit.html', {})

## modifie le dépot
@login_required
def editRepository(request, pk=None):

    repository = get_object_or_404(Repository, pk=pk)

    if request.method == 'POST':
        form = EditRepositoryForm(request.POST, request.FILES)

        if form.is_valid():

            repository.name = form.cleaned_data['name']
            repository.url = form.cleaned_data['url']
            repository.username = form.cleaned_data['login']
            repository.password = form.cleaned_data['password']
            repository.scoreAuthor = form.cleaned_data['scoreAuthor']

            repository.save()

            messages.add_message(request, messages.INFO, 'Le dépot à été modifié.')

            return redirect('repository-search',)

    else:

        form = EditRepositoryForm(instance=repository, initial='',)


    return render(request, 'repository/editRepository.html', {'form': form, 'repository': repository,})

## supprime le dépot
@login_required
def deleteRepository(request, pk=None):

    repository = get_object_or_404(Repository, pk=pk)

    if request.method == 'POST':
        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            message = form.cleaned_data['comment']
            file = request.FILES['file']
            branch = form.cleaned_data['branch']
            reference = 'refs/heads/master'

            repository.delete()

            return redirect('repository-search',)

    else:

        form = AddFileForm(initial='',)


    return render(request, 'repository/deleteRepository.html', {'form': form, 'repository': repository,})

## Créer une branche dans le dépot
@login_required
def createBranch(request, pk=None):

    repository = get_object_or_404(Repository, pk=pk)
    commits = get_list_or_404(Commit, repository=repository.id)

    # liste des branches
    branches = []
    for commit in commits:
        if not commit.branch in branches:
            branches.append((commit.branch, commit.branch))


    if request.method == 'POST':
        form = createBranchForm(request.POST, request.FILES)
        form.fields['parent_branch'].choices = branches

        if form.is_valid():
            name = form.cleaned_data['name']
            parent_branch = form.cleaned_data['parent_branch']

            if name in branches:
                raise forms.ValidationError("La branche existe déjâ.")
            if parent_branch not in branches:
                raise forms.ValidationError("La branche n\'existe pas.")

            # création branche
            git = gitlab.Gitlab(settings.GITLAB_URL, settings.GITLAB_TOKEN)
            
            git.createbranch(repository.gitlabId, name, parent_branch)

            messages.add_message(request, messages.INFO, 'La branche à été enregistré, elle sera créé lors de la prochaine mise à jour.')

            return redirect('repository-search',)

    else:

        form = createBranchForm(initial='',)
        form.fields['parent_branch'].choices = branches


    return render(request, 'repository/createBranch.html', {'form': form, 'repository': repository,})


## suprimme une branche dans le dépot
@login_required
def deleteBranch(request, pk=None):

    repository = get_object_or_404(Repository, pk=pk)

    if request.method == 'POST':
        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            message = form.cleaned_data['comment']
            file = request.FILES['file']
            branch = form.cleaned_data['branch']
            reference = 'refs/heads/master'

            temporary_folder = tempfile.mkdtemp()
            print(temporary_folder)
            cred = pygit2.UserPass('banco29510@gmail.com', 'antoine29510')
            repo = pygit2.clone_repository('https://gitlab.com/banco29510/rrrr.git', temporary_folder, bare=False, credentials=cred)

            return redirect('repository-search',)

    else:

        form = AddFileForm(initial='',)


    return render(request, 'repository/deleteRepository.html', {'form': form, 'repository': repository,})

##
@login_required
def changeCommitVisibility(request, pk=None, boolean=True):

    commit = get_object_or_404(Commit, pk=pk)

    commit.visible = boolean
    commit.save()

    if commit.visible == True:
        messages.add_message(request, messages.INFO, 'Le commit est visible.')
    else:
        messages.add_message(request, messages.INFO, 'Le commit est invisible.')

    return redirect('repository-search',)
    
    
## affiche la liste des dépot demandé en téléchargement
@login_required
def listDownload(request):
    
    listDownload = DownloadUser.objects.filter(user=request.user).order_by('-dateUpload')
    
    return render(request, 'repository/listDownload.html', {'user': request.user, 'listDownload': listDownload, })
    
    
## affiche le formulaire pour tagger un commit
@login_required
def tagCommit(request, commit=None):
    commit = get_object_or_404(Commit, pk=pk)
    
    return render(request, 'repository/tagCommit.html', {'user': request.user,})
    
## met a jour la base de donnée de façon manuel
@login_required
def updateDatabase(request, pk=None):

    repository = get_object_or_404(Repository, pk=pk)
        
    ampq_updateDatabase.delay(gitlabId=repository.gitlabId) 
                
    messages.add_message(request, messages.INFO, 'La mise à jour sera effectué sous peu.')

    return redirect('repository-showRepositoryDeveloppement', pk=repository.id)

