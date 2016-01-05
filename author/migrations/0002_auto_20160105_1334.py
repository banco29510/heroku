# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='deathDate',
            field=models.DateField(null=True, verbose_name=b'Date de d\xc3\xa9c\xc3\xa8s', blank=True),
        ),
    ]
