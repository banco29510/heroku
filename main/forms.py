from django import *
from django.forms import ModelForm
from captcha.fields import ReCaptchaField

import datetime, os, sys

from repository.models import *
from instrument.models import *
from software.models import *
from author.models import *


class LoginForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Nom ")
    password = forms.CharField(max_length=100, required=True, label="Mot de passe", widget=forms.PasswordInput)
    
class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Nom ")
    password = forms.CharField(max_length=100, required=True, label="Mot de passe", widget=forms.PasswordInput)
    repassword = forms.CharField(max_length=100, required=True, label="Mot de passe (confirmation)", widget=forms.PasswordInput)
    mail = forms.CharField(max_length=100, required=True, label="Mail")
    captcha = ReCaptchaField()
