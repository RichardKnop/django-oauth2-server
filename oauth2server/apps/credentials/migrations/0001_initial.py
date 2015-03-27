# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OAuthClient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=160)),
                ('client_id', models.CharField(unique=True, max_length=254, validators=[django.core.validators.EmailValidator()])),
                ('redirect_uri', models.CharField(max_length=200, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OAuthUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=160)),
                ('email', models.CharField(unique=True, max_length=254, validators=[django.core.validators.EmailValidator()])),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
