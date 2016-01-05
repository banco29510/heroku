# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0005_auto_20151007_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commit',
            name='author',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='commit',
            name='size',
            field=models.IntegerField(default=None, verbose_name='Taille', null=True),
        ),
        migrations.AlterField(
            model_name='commit',
            name='tag',
            field=models.CharField(default=None, max_length=100, null=True),
        ),
    ]
