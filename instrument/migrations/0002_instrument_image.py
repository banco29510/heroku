# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-17 11:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instrument', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrument',
            name='image',
            field=models.ImageField(null=True, upload_to='media'),
        ),
    ]
