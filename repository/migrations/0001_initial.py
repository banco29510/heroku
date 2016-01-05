# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Repository',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(null=True, max_length=1000)),
                ('login', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
                ('size', models.IntegerField(null=True)),
                ('scoreAuthor', models.ForeignKey(null=True, to='author.Author')),
            ],
        ),
    ]
