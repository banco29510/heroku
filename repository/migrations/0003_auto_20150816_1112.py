# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0002_auto_20150814_1225'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commit',
            old_name='comment',
            new_name='message',
        ),
    ]
