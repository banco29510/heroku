# -*- coding: utf-8 -*-
##
# \file forms.py
# \brief Software forms
# \date 24/05/15
#
from django import forms
from django.forms import ModelForm, Textarea

import datetime

from software.models import *
from licence.models import *

##
# \brief Formulaire# \author A. H.
#
class CreateSoftwareForm(forms.Form):

    name = forms.CharField(label="Nom", max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Nom','class':'form-control input-xlarge','onChange':'autoComplete()'}) )
    extension = forms.CharField(label="Extension", max_length=20, required=False, widget=forms.TextInput(attrs={'placeholder':'Extension','class':'form-control input-xlarge','onChange':'autoComplete()'}) )
    licence = forms.ModelChoiceField(queryset=Licence.objects.all(),  required=False, widget=forms.Select(attrs={'placeholder':'','class':'form-control input-xlarge'}) )

##
# \brief Formulaire
# \author A. H.
#
class UpdateSoftwareForm(forms.Form):
    name = forms.CharField(label="Nom", max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Nom','class':'form-control input-xlarge','onChange':'autoComplete()'}) )
    extension = forms.CharField(label="Extension", max_length=20, required=True, widget=forms.TextInput(attrs={'placeholder':'Extension','class':'form-control input-xlarge','onChange':'autoComplete()'}) )
    licence = forms.ModelChoiceField(queryset=Licence.objects.all(),  required=False, widget=forms.Select(attrs={'placeholder':'','class':'form-control input-xlarge'}) )

##
# \brief Formulaire
# \author A. H.
#
class DeleteSoftwareForm(forms.Form):
    pass


