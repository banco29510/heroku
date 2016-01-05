# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0004_commit_deprecated'),
    ]

    operations = [
        migrations.AddField(
            model_name='commit',
            name='author',
            field=models.CharField(null=True, max_length=100),
        ),
        migrations.AddField(
            model_name='commit',
            name='size',
            field=models.IntegerField(verbose_name='Taille', null=True),
        ),
        migrations.AddField(
            model_name='commit',
            name='tag',
            field=models.CharField(null=True, max_length=100),
        ),
    ]
