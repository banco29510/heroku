from django import *
from django.forms import ModelForm
from captcha.fields import ReCaptchaField

import datetime, os, sys

from repository.models import *
from instrument.models import *
from software.models import *
from author.models import *

    
class EditUserForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label="Nom d'utilisateur")
    firstName = forms.CharField(max_length=100, required=True, label="Prénom ")
    lastName = forms.CharField(max_length=100, required=True, label="Nom ")
    
