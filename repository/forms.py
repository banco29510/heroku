# -*- coding: utf-8 -*-
from django import *
from django.forms import ModelForm

import datetime, os, sys

from repository.models import *
from instrument.models import *
from software.models import *
from author.models import *

##
# \brief Formulaire
# \author A. H.
#
class RepositoryForm(ModelForm):
    class Meta:
        model = Repository
        exclude = ['size']


    def clean_name(self):
        name = self.cleaned_data['name']
        return name.capitalize()
        
class NewRepositoryForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Nom ")
    scoreAuthor = forms.ModelChoiceField(queryset=Author.objects.all(), label="Auteur", required=True)
        

class SearchForm(forms.Form):
    name = forms.CharField(max_length=100, required=False, label="Nom ")
    instrument = forms.ModelChoiceField(queryset=Instrument.objects.all(), label="Instrument", required=False)
    author = forms.ModelChoiceField(queryset=Author.objects.all(), label="Auteur", required=False)
    software = forms.ModelChoiceField(queryset=Software.objects.all(), label="Logiciel", required=False)

##
# \brief Formulaire de ajout d'un fichier
# \author A. H.
#
class AddFileForm(forms.Form):

    comment = forms.CharField(
        label="Commentaire",
        max_length=100,
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder':'Commentaire','class':'form-control input-xlarge'}
        )
    )
    file = forms.FileField(
        label = 'Sélectionner un fichier',
        required = True,
    )

    branch = forms.ChoiceField(
        label="Branche",
        required=False,
        widget=forms.Select(
            attrs={'placeholder':'Branche','class':'form-control input-xlarge',}
        )
    )

    def clean_comment(self):
        comment = self.cleaned_data['comment'].strip().capitalize()
        return comment

# Supression d'un fichier
class DeleteFileForm(forms.Form):
    pass

##
# \brief Formulaire de ajout d'un fichier
# \author A. H.
#
class createBranchForm(forms.Form):

    name = forms.CharField(
        label="Nom",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder':'Nom','class':'form-control input-xlarge'}
        )
    )

    parent_branch = forms.ChoiceField(
        label="Branche parente",
        required=True,
        widget=forms.Select(
            attrs={'placeholder':'Branche parente','class':'form-control input-xlarge',}
        )
    )

    def clean_name(self):
        name = self.cleaned_data['name'].strip().capitalize()
        return name
        
##
# \brief Formulaire suppression branche
# \author A. H.
#
class deleteBranchForm(forms.Form):

    branch = forms.ChoiceField(
        label="Branche",
        required=True,
        widget=forms.Select(
            attrs={'placeholder':'Branche','class':'form-control input-xlarge',}
        )
    )

##
# \brief Formulaire suppression branche
# \author A. H.
#
class MergeBranchForm(forms.Form):

    source_branch = forms.ChoiceField(
        label="Branche source",
        required=True,
        widget=forms.Select(
            attrs={'placeholder':'Branche à fusionner','class':'form-control input-xlarge',}
        )
    )
    
    merge_branch = forms.ChoiceField(
        label="Branche fusionner",
        required=True,
        widget=forms.Select(
            attrs={'placeholder':'Branche qui va recevoir la fusion','class':'form-control input-xlarge',}
        )
    )

##
# \brief Formulaire de ajout d'un fichier
# \author A. H.
#
class EditRepositoryForm(ModelForm):
    class Meta:
         model = Repository
         exclude = ('size',)
         
##
# \brief Formulaire de conversion des fichiers
# \author A. H.
#
class ConvertFileForm(forms.Form):

    extension = forms.ChoiceField(
        label="Extension",
        required=True,
        widget=forms.Select(
            attrs={'placeholder':'Extension','class':'form-control input-xlarge',}
        )
    )

##
# \brief Formulaire suppression dépot
# \author A. H.
#
class DeleteRepositoryForm(forms.Form):
    pass

##
# \brief editiot ndes fichiers markdown
# \author A. H.
#
class EditFileMarkdownForm(forms.Form):
   
    source = forms.CharField(widget=forms.Textarea(attrs={'rows': 20, 'cols': 80}))
    
