# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('licence', '0001_initial'),
        ('software', '0001_initial'),
        ('instrument', '0001_initial'),
        ('repository', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commit',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('comment', models.CharField(max_length=10000)),
                ('date', models.DateTimeField(null=True)),
                ('branch', models.CharField(null=True, default=None, max_length=100)),
                ('hashCommit', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('hashFile', models.CharField(default=None, max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('size', models.IntegerField(null=True)),
                ('difficultLevel', models.IntegerField(null=True)),
                ('commits', models.ManyToManyField(to='repository.Commit')),
                ('instrument', models.ManyToManyField(to='instrument.Instrument')),
                ('licence', models.ForeignKey(null=True, to='licence.Licence')),
                ('software', models.ForeignKey(null=True, to='software.Software')),
            ],
        ),
        migrations.AlterField(
            model_name='repository',
            name='login',
            field=models.CharField(verbose_name="Nom d'utilisateur", max_length=100),
        ),
        migrations.AlterField(
            model_name='repository',
            name='name',
            field=models.CharField(verbose_name='Nom', max_length=100),
        ),
        migrations.AlterField(
            model_name='repository',
            name='password',
            field=models.CharField(verbose_name='Mot de passe', max_length=100),
        ),
        migrations.AlterField(
            model_name='repository',
            name='scoreAuthor',
            field=models.ForeignKey(null=True, verbose_name='Auteur', to='author.Author'),
        ),
        migrations.AlterField(
            model_name='repository',
            name='size',
            field=models.IntegerField(null=True, verbose_name='Taille'),
        ),
        migrations.AlterField(
            model_name='repository',
            name='url',
            field=models.CharField(null=True, verbose_name='Url', max_length=1000),
        ),
        migrations.AddField(
            model_name='commit',
            name='repository',
            field=models.ForeignKey(to='repository.Repository'),
        ),
    ]
