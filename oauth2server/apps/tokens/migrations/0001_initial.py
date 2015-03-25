# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('credentials', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OAuthAccessToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(unique=True, max_length=40)),
                ('expires_at', models.DateField()),
                ('scope', models.CharField(default=b'', max_length=50)),
                ('client', models.ForeignKey(to='credentials.OAuthClient')),
                ('user', models.ForeignKey(to='credentials.OAuthUser', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OAuthAuthorizationCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=40)),
                ('expires_at', models.DateField()),
                ('redirect_uri', models.CharField(default=b'', max_length=200)),
                ('scope', models.CharField(default=b'', max_length=50)),
                ('client', models.ForeignKey(to='credentials.OAuthClient')),
                ('user', models.ForeignKey(to='credentials.OAuthUser', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OAuthRefreshTokenToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(unique=True, max_length=40)),
                ('expires_at', models.DateField()),
                ('scope', models.CharField(default=b'', max_length=50)),
                ('client', models.ForeignKey(to='credentials.OAuthClient')),
                ('user', models.ForeignKey(to='credentials.OAuthUser', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
