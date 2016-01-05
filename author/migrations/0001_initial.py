# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=75)),
                ('birthDate', models.DateField(null=True, blank=True, verbose_name='Date de naissance')),
                ('deathDate', models.DateField(null=True, blank=True, verbose_name='Date de décès')),
                ('nationality', models.TextField(max_length=100, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
