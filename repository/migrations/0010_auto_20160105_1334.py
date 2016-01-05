# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0009_temporaryfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='temporaryfile',
            name='file',
            field=models.FileField(upload_to=b'media/'),
        ),
    ]
