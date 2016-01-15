# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User

import os, json

from licence.models import *
from instrument.models import *
from software.models import *
from author.models import *


##
# \brief Model des dépots
# \author A. H.
# \class
#
class Repository(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    scoreAuthor = models.ForeignKey(Author, null=True, verbose_name="Auteur")
    size = models.IntegerField(null=True, verbose_name="Taille")
    gitlabId = models.IntegerField(null=True,)

    ##
    #
    def __str__(self):
        return u"%s" % self.name

##
# \brief Model des branches
# \author A. H.
# \class
#
class Branche(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    repository = models.ForeignKey(Repository, null=True, verbose_name="Dépot")

    ##
    #
    def __str__(self):
        return u"%s" % self.name



        
##
# \brief Révision des commits
# \author A. H.
# \class
#
class Commit(models.Model):
    repository = models.ForeignKey(Repository, null=False)
    message = models.CharField(max_length=10000)
    date = models.DateTimeField(null=True,)
    branch = models.ForeignKey(Branche, null=True, verbose_name="Dépot")
    hashCommit = models.CharField(max_length=100)
    deprecated = models.BooleanField(default=False)
    visible = models.BooleanField(default=True)
    lock = models.BooleanField(default=False)
    author = models.CharField(max_length=100, null=True , default=None)
    size = models.IntegerField(null=True, verbose_name="Taille", default=None)

    ##
    #
    def __str__(self):
        return u"%s" % self.message


##
# \brief Model des tags
# \author A. H.
# \class
#
class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nom")
    commit = models.ForeignKey(Commit, null=True, verbose_name="Commit")

    ##
    #
    def __str__(self):
        return u"%s" % self.name
        
##
# \brief Liste des fichiers
# \author A. H.
# \class File(models.Model):
#
class File(models.Model):
    hashFile = models.CharField(max_length=100, default=None)
    name = models.CharField(max_length=100)
    size = models.IntegerField(null=True,)
    commit = models.ForeignKey(Commit, null=False)
    instrument = models.ManyToManyField(Instrument,)
    software = models.ForeignKey(Software, null=True)
    licence = models.ForeignKey(Licence, null=True)

    ##
    #
    def __str__(self):
        return "%s" % self.name

    ##
    #
    def extension(self):
        return os.path.splitext(self.name)[1].lower()

    ##
    #
    def nameWithoutExtension(self):
        return os.path.splitext(self.name)[0]

##
# \brief Liste des fichiers temporaire (upload et download)
# \author A. H.
# \class TemporaryFile(models.Model):
#
class TemporaryFile(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='media/')
    dateUpload = models.DateTimeField(auto_now_add=True)
    dateDelete = models.DateTimeField(auto_now_add=True)

    ##
    #
    def __str__(self):
        return "%s" % self.name
        
    def filename(self):
        return os.path.basename(self.file.name)


##
# \brief Téléchargement demandé par les utilisateurs
# \author A. H.
# \class DownloadUser(models.Model):
#
class DownloadUser(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, unique=False)
    file = models.FileField(upload_to='media/')
    dateUpload = models.DateTimeField(auto_now_add=True)

    ##
    #
    def __str__(self):
        return "%s" % self.name
        
    

