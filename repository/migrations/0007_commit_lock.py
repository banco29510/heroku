# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0006_auto_20151007_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='commit',
            name='lock',
            field=models.BooleanField(default=False),
        ),
    ]
