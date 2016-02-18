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
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import cache_page
from django.shortcuts import get_object_or_404, get_list_or_404, redirect, render
from django.contrib.auth import authenticate
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.edit import *
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

import pprint, tempfile, os, sys, json, datetime, time, mimetypes, zipfile, shutil, base64, subprocess

import cloudconvert

from gitlab import *
from github import Github

from celery import Celery
from celery import chain, group, chord
from .tasks import *


from repository.models import *
from repository.forms import *

from repository.tasks import *

## \brief recherche des partitions
# \author A. H.
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

## \brief créer une partition
# \author A. H.
@login_required
def newScore(request):
    
    if request.method == 'POST':
        form = NewRepositoryForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name'].replace(' ', '-')
            scoreAuthor = form.cleaned_data['scoreAuthor']

            # creation dépot github
            g = Github(settings.GIT_USERNAME, settings.GIT_PASSWORD)
            user = g.get_user()
            repo = user.create_repo(name)
        
            
            # création du dépot dans la bdd
            repository = Repository()
            repository.name = name
            repository.scoreAuthor = scoreAuthor
            repository.url = 'https://'+settings.GIT_USERNAME+':'+settings.GIT_PASSWORD+'@github.com/banco29510/'+name+'.git'
            repository.username = settings.GIT_USERNAME
            repository.password = settings.GIT_PASSWORD
            repository.save()
            
            repository = Repository.objects.get(name=name)
            
            ampq_createRepository.delay(repository.id)
            ampq_updateDatabase.delay(repository.id) # update database

            
            messages.add_message(request, messages.INFO, 'Le dépot à été crée. Première révision lors de la prochaine mise à jour.')
            return redirect('repository-search',)

    else:
        form = NewRepositoryForm(initial={})


    return render(request, 'repository/newScore.html', {'form': form,})

## \brief ajoute un fichier
# \author A. H.
@login_required
def addFile(request, pk=None):

    repository = get_object_or_404(Repository, pk=pk)
    branches = get_list_or_404(Branche, repository=repository)
    
    try:
        commits = get_list_or_404(Commit, repository=repository.id)
    except:
        commits = []
    
    list_branch = []
    for branch in branches:
        list_branch.append((branch, str(branch).capitalize() ))
        
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
            
            ampq_addFile.delay(id=repository.id, file=TempFile, message=message, branch=branch)
            ampq_updateDatabase.delay(pk=repository.id) 
                
            messages.add_message(request, messages.INFO, 'Le fichier à été sauvegardé, la mise à jour sera effectué sous peu.')

            return redirect('repository-showRepositoryDeveloppement', pk=repository.id)


    else:

        form = AddFileForm(initial='',)
        form.fields['branch'].choices = branches



    return render(request, 'repository/addFile.html', {'form': form, 'repository': repository,})
    
## \brief voir le depot en production avec juste la derniere version
# \author A. H.
@login_required
def showRepositoryProduction(request, pk=None):

    repository = get_object_or_404(Repository, pk=pk)
    ampq_updateDatabase.delay(repository.id)
    
    
    try:
        commits = Commit.objects.filter(repository=repository).order_by('-date')
        commit = commits[0]
    except:
        commit = []
        
        
    try:
        files = File.objects.filter(commit = commits[0])
        size_commit = 0
        for file in files:
            size_commit = size_commit + file.size
    except:
        files = []
        size_commit = 0
        
    try:
        readme = File.objects.get(commit = commits[0], name="readme.md")
    except:
        readme = []
        
    print(readme)

    return render(request, 'repository/showRepositoryProduction.html', {'repository': repository, 'files': files, 'readme': readme, 'commit': commit, 'size_commit': size_commit,})

## \brief  Voir un fichier
# \author A. H.
@login_required
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
    
    temp = tempfile.mkdtemp()
    repo = Repo.clone_from(repository.url, temp, branch=commit.branch)
    
    repo.git.checkout(commit.hash)
    
    fichier = open(temp+'/'+file.name, 'rb')
    content = fichier.read()
    fichier.close()

    response = HttpResponse()

    response['Content-Type'] = mimetype=mimetypes.guess_type(str(file.name))[0]
    response['Content-Disposition'] = 'inline; filename='+str(file.name)
    response['Content-Length'] = os.path.getsize(repo.working_tree_dir+'/'+file.name)
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
    temp = tempfile.mkdtemp()
    print(temporary_folder)
    
    repo = Repo.clone_from(repository.url, temp, branch=commit.branch)
    
    repo.git.checkout(commit.hash)
    
    

    response = HttpResponse()

    response['Content-Type'] = mimetype=mimetypes.guess_type(repository.name+'.zip')[0]
    response['Content-Disposition'] = 'attachment; filename='+repository.name+'.zip'
    response['Content-Length'] = os.path.getsize(temporary_folder+'/'+repository.name+'.zip')
    response.write(open(temporary_folder+'/'+repository.name+'.zip', 'rb').read())

    return response


## \brief Voir la page du dépot en developpement
# \author A. H.
@login_required
def showRepositoryDeveloppement(request, pk=None):

    repository = get_object_or_404(Repository, pk=pk)
    
    try:
        branches = Branche.objects.filter(repository=repository)
    except:
        branches = []
    
    try:
        if request.GET.get('commit'):
            commits = Commit.objects.filter(repository=repository, pk=request.GET['commit']) 
        else:
            commits = Commit.objects.filter(repository=repository).order_by('-date')
            
        commit = commits[0]
    except:
        commits = []
        commit = []
        
    try:
        files = File.objects.filter(commit = commits[0])
        size_commit = 0
        for file in files:
            size_commit = size_commit + file.size
        
    except:
        files = []
        size_commit = 0
        
    try:
        readme = File.objects.get(commit = commits[0], name = "readme.md")
        tags = Tag.objects.filter(commit = commits[0])
    except:
        readme = []
        tags = []
        

    return render(request, 'repository/showRepositoryDeveloppement.html', {'repository': repository, 
                                                                            'files': files, 
                                                                            'commit': commit, 
                                                                            'size_commit': size_commit,
                                                                            'readme': readme,
                                                                            'commits': commits,
                                                                            'tags': tags,
                                                                            'branches':branches,
                                                                            })


## \brief renomme un fichier
# \author A. H.
@login_required
@csrf_exempt
def renameFile(request, pk=None, pk_commit=None):

    file = get_object_or_404(File, pk=pk)
    commit = get_object_or_404(Commit, pk=pk_commit)
    repository = commit.repository

    ampq_renameFile.delay(repository.id, file, request.POST.get("name", ""))
    ampq_updateDatabase.delay(repository.id)

    messages.add_message(request, messages.INFO, 'Le fichier est renommé, il sera pris en compte lors de la prochaine mise à jour.')
    
    return redirect('repository-showRepositoryDeveloppement', repository.id)
    
## \brief renomme un fichier
# \author A. H.
@login_required
@csrf_exempt
def replaceFile(request, pk=None,):

    file = get_object_or_404(File, pk=pk)
    
    #ampq_replaceFile.delay(repository.id, file, )
    ampq_updateDatabase.delay(file.commit.repository.id)

    messages.add_message(request, messages.INFO, 'Le fichier est remplacé, il sera pris en compte lors de la prochaine mise à jour.')
    
    return redirect('repository-showRepositoryDeveloppement', file.commit.repository.id)

## \brief suprimme un fichier
# \author A. H.
@login_required
def deleteFile(request, pk=None, pk_commit=None):

    file = get_object_or_404(File, pk=pk)
    commit = get_object_or_404(Commit, pk=pk_commit)
    print(file.name)
    print(commit.message)
    
    if request.method == 'POST':
        form = DeleteFileForm(request.POST, request.FILES)

        if form.is_valid():
            
            ampq_deleteFile.delay(commit.repository.id, file, "Supression du fichier "+str(file.name), file.commit.branch.name)
            ampq_updateDatabase.delay(pk=commit.repository.id) 
                
            messages.add_message(request, messages.INFO, 'Le fichier à été suprimmé, la mise à jour sera effectué sous peu.')

            return redirect('repository-showRepositoryDeveloppement', pk=commit.repository.id)


    else:

        form = DeleteFileForm(initial='',)
        


    return render(request, 'repository/deleteFile.html', {'form': form, 'repository': commit.repository,})

## \brief telechargement du fichier
# \author A. H.
# \fn def downloadFile(request, pk=None,):
# \param[in] pk=None id du téléchargement
# \return le fichier
#
@login_required
def downloadFile(request, pk=None,):
    
    download = DownloadUser.objects.get(pk=pk, user=request.user)
    
    response = HttpResponse()

    response['Content-Type'] = mimetype=mimetypes.guess_type(download.name)
    response['Content-Disposition'] = 'attachment; filename='+str(download.name)
    response['Content-Length'] = download.file.size
    response.write(download.file.read())

    return response

## \brief liste des commits et des branches
# \author A. H.
@login_required
def listCommits(request, pk=None):

    repository = Repository.objects.get(pk=pk)
    branches = Branche.objects.filter(repository=repository)
    
    try:
        commits = get_list_or_404(Commit.objects.order_by('-date'), repository=repository)
    except:
        commits = []
        
    # création form pour créer une branche
    form_branches = []
    for branche in branches:
        form_branches.append((branche.name,branche.name.capitalize()))
        
    form = createBranchForm(initial='',)
    form.fields['parent_branch'].choices = form_branches
    form.fields['parent_branch'].initial = [0]
    
    form_deleteBranch = deleteBranchForm(initial='',)
    form_deleteBranch.fields['branch'].choices = form_branches
    form_deleteBranch.fields['branch'].initial = [0]
    
    # création form pour fusionner les branches
    form_mergeBranch = MergeBranchForm(initial='',)
    form_mergeBranch.fields['source_branch'].choices = form_branches
    form_mergeBranch.fields['source_branch'].initial = [0]
    form_mergeBranch.fields['merge_branch'].choices = form_branches
    form_mergeBranch.fields['merge_branch'].initial = [1]
    
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
        'form_deleteBranch': form_deleteBranch,
        'form_mergeBranch' : form_mergeBranch,
    })

## \brief liste des contributeurs et statistiques
# \author A. H.
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

## \brief supprime un commit
# \author A. H.
@login_required
def deleteCommit(request, pk=None):

    commit = get_object_or_404(Commit, pk=pk)
    
    messages.add_message(request, messages.INFO, 'L\' opération est en cours, le commit sera suprimmé sous peu.')

    return render(request, 'repository/deleteCommit.html', {})

## \brief change la version en déprécié
# \author A. H.
@login_required
def changeDeprecated(request, pk=None, boolean=True):

    commit = get_object_or_404(Commit, pk=pk)
    
    if int(boolean) == 0:
        boolean = False
    else:
        boolean = True
      
    commit.deprecated = boolean
    commit.save()

    if commit.deprecated == True:
        messages.add_message(request, messages.INFO, 'Le dépot est déprécié.')
    else:
        messages.add_message(request, messages.INFO, 'Le dépot n\'est plus déprécié.')


    return redirect('repository-showRepositoryDeveloppement', commit.repository.id)

## \brief
@login_required
def restartRepositoryByOldCommit(request, pk=None):

    commit = get_object_or_404(Commit, pk=pk)

    temporary_folder = tempfile.mkdtemp()
    print(temporary_folder)
    
    return render(request, 'repository/restartRepositoryByOldCommit.html', {})

## \brief merge deux commits
# \author A. H.
@login_required
@csrf_exempt
def mergeCommit(request, pk=None):

    repository = get_object_or_404(Repository, pk=pk)
    source_branch = request.POST.get('source_branch', None) 
    merge_branch = request.POST.get('merge_branch', None) 
    
    ampq_mergeBranch.delay(repository.id, source_branch, merge_branch)
    ampq_updateDatabase.delay(repository.id)
    
    messages.add_message(request, messages.INFO, 'La fusion sera effectué à la prochaine mise à jour.')

    return redirect('repository-listCommits', repository.id)

## \brief modifie le dépot
# \author A. H.
@login_required
@staff_member_required
def editRepository(request, pk=None):

    repository = get_object_or_404(Repository, pk=pk)

    if request.method == 'POST':
        form = EditRepositoryForm(request.POST, request.FILES)

        if form.is_valid():

            repository.name = form.cleaned_data['name']
            repository.url = form.cleaned_data['url']
            repository.username = form.cleaned_data['name']
            repository.password = form.cleaned_data['password']
            repository.scoreAuthor = form.cleaned_data['scoreAuthor']

            repository.save()

            messages.add_message(request, messages.INFO, 'Le dépot à été modifié.')

            return redirect('repository-showRepositoryDeveloppement', repository.id)

    else:

        form = EditRepositoryForm(instance=repository, initial='',)


    return render(request, 'repository/editRepository.html', {'form': form, 'repository': repository,})

## \brief supprime le dépot
# \author A. H.
@login_required
@staff_member_required
def deleteRepository(request, pk=None):

    repository = get_object_or_404(Repository, pk=pk)

    if request.method == 'POST':
        form = DeleteRepositoryForm(request.POST)

        if form.is_valid():
            
            g = Github(settings.GIT_USERNAME, settings.GIT_PASSWORD)
            user = g.get_user()
            
            user.get_repo(repository.name).delete()
            
            repository.delete()
            
            messages.add_message(request, messages.INFO, 'Le dépot à été supprimé.')

            return redirect('repository-search',)

    else:

        form = DeleteRepositoryForm(initial='',)


    return render(request, 'repository/deleteRepository.html', {'form': form, 'repository': repository,})

## \brief Créer une branche dans le dépot
# \author A. H.
@login_required
@csrf_exempt
def createBranch(request, pk=None):

    repository = get_object_or_404(Repository, pk=pk)
    commits = get_list_or_404(Commit, repository=repository.id)
    branches = get_list_or_404(Branche, repository=repository.id)
    
    # création branche
    ampq_createBranch.delay(repository.id, request.POST.get("name", ""), request.POST.get("parent_branch", ""))

    messages.add_message(request, messages.INFO, 'La branche à été enregistré, elle sera créé lors de la prochaine mise à jour.')

    return redirect('repository-showRepositoryDeveloppement', repository.id)

## \brief suprimme une branche dans le dépot
@login_required
def deleteBranch(request, pk=None):

    repository = get_object_or_404(Repository, pk=pk)

    if request.method == 'POST':
        form = AddFileForm(request.POST, request.FILES)

        if form.is_valid():
            message = form.cleaned_data['comment']
            file = request.FILES['file']
            branch = form.cleaned_data['branch']

            return redirect('repository-search',)

    else:

        form = AddFileForm(initial='',)


    return render(request, 'repository/deleteRepository.html', {'form': form, 'repository': repository,})

## \brief
# \author A. H.
@login_required
def changeCommitVisibility(request, pk=None, boolean=True):

    commit = get_object_or_404(Commit, pk=pk)

    print(boolean)
    
    if int(boolean) == 0:
        boolean = False
    else:
        boolean = True
        
    print(boolean)
        
    commit.visible = boolean
    commit.save()

    if commit.visible == True:
        messages.add_message(request, messages.INFO, 'Le commit est visible.')
    else:
        messages.add_message(request, messages.INFO, 'Le commit est invisible.')

    return redirect('repository-showRepositoryDeveloppement', commit.repository.id)
    
## \brief affiche la liste des dépot demandé en téléchargement
# \author A. H.
@login_required
def listDownload(request):
    
    listDownload = DownloadUser.objects.filter(user=request.user).order_by('-dateUpload')
    
    paginator = Paginator(listDownload, 20)

    page = request.GET.get('page', 1)
    try:
        listDownload = paginator.page(page)
    except PageNotAnInteger:
        listDownload = paginator.page(1)
    except EmptyPage:
        listDownload = paginator.page(paginator.num_pages)
    
    return render(request, 'repository/listDownload.html', {'user': request.user, 'listDownload': listDownload, })
    
## \brief affiche le formulaire pour tagger un commit
# \author A. H.
@login_required
@csrf_exempt
def tagCommit(request, pk=None):
    commit = get_object_or_404(Commit, pk=pk)
    repository = commit.repository
    print(request.POST.get("name", ""))
    
    ampq_tagCommit.delay(repository.id, commit.id, request.POST.get("name", "") )
    ampq_updateDatabase.delay(repository.id)
    
    messages.add_message(request, messages.INFO, 'Le tag est enregistré, il sera pris en compte lors de la prochaine mise à jour.')
    
    return redirect('repository-showRepositoryDeveloppement', repository.id)
    
## \brief met a jour la base de donnée de façon manuel
# \author A. H.
@login_required
def updateDatabase(request, pk=None):

    repository = get_object_or_404(Repository, pk=pk)
        
    ampq_updateDatabase.delay(gitlabId=repository.id) 
                
    messages.add_message(request, messages.INFO, 'La mise à jour sera effectué sous peu.')

    return redirect('repository-showRepositoryDeveloppement', pk=repository.id)

## \brief confirme le telechargement du dépot
# \author A. H.
@login_required
def warningDownloadRepository(request, pk=None,):

    repository = get_object_or_404(Repository, pk=pk)

    ampq_downloadRepository.delay(repository.id, request.user)

    return render(request, 'repository/warningDownloadRepository.html', {})

## \brief confirme le telechargement du fichier
# \author A. H.
@login_required
def warningDownloadCommit(request, pk=None, pk_commit=None):
    
    repository = get_object_or_404(Repository, pk=pk)
    commit = get_object_or_404(Commit, pk=pk_commit)

    ampq_downloadCommit.delay(repository.id, request.user, commit)

    return render(request, 'repository/warningDownloadCommit.html', { })
    
## \brief  confirme le telechargement du fichier
# \author A. H.
@login_required
def warningDownloadFile(request, pk=None, pk_commit=None):

    file = get_object_or_404(File, pk=pk)
    commit = get_object_or_404(Commit, pk=pk_commit)

    ampq_downloadFile.delay(commit.repository.id, file, request.user)
    
    return render(request, 'repository/warningDownloadFile.html', {})
    
## \brief edit les fichiers markdown
# \author A. H.
@login_required
def editMarkdown(request, pk=None, pk_file=None):

    file = get_object_or_404(File, pk=pk_file)
    commit = file.commit
    repository = commit.repository
    source = ''
    
    
    if request.method == 'POST':
        form = EditFileMarkdownForm(request.POST)

        if form.is_valid():

            form_extension = form.cleaned_data['source']
            
            messages.add_message(request, messages.INFO, 'La conversion sera ajouté au dépot lors de la prochaine mise à jour.')

            return redirect('repository-showRepositoryDeveloppement', file.commit.repository.id)

    else:

        form = EditFileMarkdownForm(initial={'source': source, },)
        
    

    return render(request, 'repository/editMarkdown.html', {'form': form, 'file': file, 'commit': file.commit,})
    
## \brief convertit les fichiers
# \author A. H.
@login_required
def convertFile(request, pk=None, ):

    file = get_object_or_404(File, pk=pk)
    commit = file.commit
    repository = commit.repository
    
    extension_texte = [('.md', 'Document markdown'), 
                      ('.txt', 'Document Texte'), ]
    
    extension_music = [('.mp3', 'Document MP3'), 
                      ('.ogg', 'Document OGG'), 
                      ('.wma', 'Document WMA'), ]
                      
    extension_image = [('.jpg', 'Image jpg'), 
                      ('.jpeg', 'Image jpeg'), 
                      ('.svg', 'Image svg'),
                      ('.png', 'Image png'),]
    
    extension_convert = [] 
    
    for extension in extension_texte:
        if extension[0] == file.extension():
            extension_convert = extension_texte
            #i = 0
            #for extension_convert in extension_convert:
            #    #extension_convert[:]
            #    i+=1
                        
    extension = file.extension()
    
    if request.method == 'POST':
        form = ConvertFileForm(request.POST)
        form.fields['extension'].choices = extension_convert

        if form.is_valid():

            form_extension = form.cleaned_data['extension'].replace('.', '') 
            
            # obtention du fichier
            temp = tempfile.mkdtemp()
    
            repo = Repo.clone_from(repository.url, temp, branch=file.commit.branch.name) # clone du dépot
    
            repo.git.checkout(file.commit.hash)
    
            #fichier = open(temp+'/'+file.name, "rb")
            #content = ContentFile(fichier.read())
            #fichier.close()
            
            # conversion ampq cloud convert
            api = cloudconvert.Api(settings.TOKEN_CLOUDCONVERT)
           
            #print(form_extension)
            #print(file.extensionWithoutDot())
            #print(open(temp+'/'+file.name, "rb"))
            #print(file.name)
            
            process = api.createProcess({
                'inputformat': file.extensionWithoutDot(),
                'outputformat': form_extension
            })
            process.start({
                'input': 'upload',
                'outputformat': form_extension,
                'wait': True,
                'file': open(temp+'/'+file.name, "rb")
            
            })
            
            process.wait()
            process.download(temp+"/"+file.nameWithoutExtension()+'.'+form_extension)
            process.delete()
            
            #print(file.nameWithoutExtension()+'.'+form_extension)
            
            # mise a jour du dépot
            convert_file = open(temp+'/'+file.nameWithoutExtension()+'.'+form_extension, "rb")
            TempFile = TemporaryFile()
            TempFile.name = file.nameWithoutExtension()+'.'+form_extension
            TempFile.file.name = file.nameWithoutExtension()+'.'+form_extension
            TempFile.file.save(file.nameWithoutExtension()+'.'+form_extension, ContentFile(convert_file.read()), save=True)
            convert_file.close()
            TempFile.save() 
            
            ampq_addFile.delay(repository.id, TempFile, 'Conversion', file.commit.branch.name)
            
            
            ampq_updateDatabase.delay(file.commit.repository.id)
            
            
            messages.add_message(request, messages.INFO, 'La conversion sera ajouté au dépot lors de la prochaine mise à jour.')

            return redirect('repository-search',)
            #return render(request, 'repository/convert.html', {'file': file, 'form': form})

    else:

        form = ConvertFileForm(initial='',)
        form.fields['extension'].choices = extension_convert

    
    return render(request, 'repository/convert.html', {'file': file, 'form': form})