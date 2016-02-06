# -*- coding: utf-8 -*-
from django import *
from django.forms import ModelForm

import datetime, os, sys

from repository.models import *
from instrument.models import *
from software.models import *
from author.models import *


class LoginForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label="Nom ")
    password = forms.CharField(max_length=100, required=True, label="Mot de passe", widget=forms.PasswordInput)
