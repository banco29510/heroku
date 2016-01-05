# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('licence', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Software',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('extension', models.CharField(max_length=100, null=True)),
                ('licence', models.OneToOneField(to='licence.Licence', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
