##
# \file depot.forms.py
# \brief Class depot forms
# \date 4 septembre 2014
#
# Class formualire en lien avec le dépot
#
from django import forms
from django.forms import ModelForm, Textarea

import datetime

from instrument.models import Instrument

##
# \brief Formulaire
# \author A. H.
#
class CreateInstrumentForm(forms.Form):

    name = forms.CharField(label="Nom", max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Nom','class':'form-control input-xlarge','onChange':'autoComplete()'}) )

##
# \brief Formulaire
# \author A. H.
#
class UpdateInstrumentForm(forms.Form):

    name = forms.CharField(label="Nom", max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder':'Nom','class':'form-control input-xlarge','onChange':'autoComplete()'}) )

##
# \brief Formulaire
# \author A. H.
#
class DeleteInstrumentForm(forms.Form):
    pass


