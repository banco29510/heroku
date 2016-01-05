# -*- coding: utf-8 -*-
##
# \file depot.forms.py
# \brief Class depot forms
# \date 19/03/2015
#
# Class formualire en lien avec les auteurs
#
from django import forms
from django.forms import ModelForm, Textarea

import datetime

from author.models import Author

##
# \brief Formulaire de création des auteurs
# \author A. H.
#
class CreateAuthorForm(forms.Form):

    name = forms.CharField(
        label="Nom",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder':'Nom','class':'form-control input-xlarge','onChange':'autoComplete()'}
        )
    )
    birthDate = forms.DateField(
        label="Date de naissance",
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder':'Date de naissance','class':'form-control input-xlarge'}
        )
    )
    deathDate = forms.DateField(
        label="Date de mort",
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder':'Date de mort','class':'form-control input-xlarge'}
        )
    )
    nationality = forms.CharField(
        label="Nationalité",
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder':'Nationalité','class':'form-control input-xlarge'}
        )
    )

##
# \brief Formulaire de mise à jour des auteurs
# \author A. H.
#
class UpdateAuthorForm(forms.Form):

    name = forms.CharField(
        label="Nom",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={'placeholder':'Nom','class':'form-control input-xlarge','onChange':'autoComplete()'}
        )
    )
    birthDate = forms.DateField(
        label="Date de naissance",
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder':'Date de naissance','class':'form-control input-xlarge'}
        )
    )
    deathDate = forms.DateField(
        label="Date de mort",
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder':'Date de mort','class':'form-control input-xlarge'}
        )
    )
    nationality = forms.CharField(
        label="Nationalité",
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder':'Nationalité','class':'form-control input-xlarge'}
        )
    )

##
# \brief Formulaire
# \author A. H.
#
class DeleteAuthorForm(forms.Form):
    pass


