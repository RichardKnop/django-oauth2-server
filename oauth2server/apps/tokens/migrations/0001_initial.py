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
                ('expires_at', models.DateTimeField()),
                ('scope', models.CharField(max_length=200, null=True)),
                ('access_token', models.CharField(unique=True, max_length=40)),
                ('client', models.ForeignKey(to='credentials.OAuthClient')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OAuthAuthorizationCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('expires_at', models.DateTimeField()),
                ('scope', models.CharField(max_length=200, null=True)),
                ('code', models.CharField(unique=True, max_length=40)),
                ('redirect_uri', models.CharField(max_length=200, null=True)),
                ('client', models.ForeignKey(to='credentials.OAuthClient')),
                ('user', models.ForeignKey(to='credentials.OAuthUser', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OAuthRefreshToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('expires_at', models.DateTimeField()),
                ('refresh_token', models.CharField(unique=True, max_length=40)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='oauthaccesstoken',
            name='refresh_token',
            field=models.OneToOneField(related_name='access_token', null=True, to='tokens.OAuthRefreshToken'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='oauthaccesstoken',
            name='user',
            field=models.ForeignKey(to='credentials.OAuthUser', null=True),
            preserve_default=True,
        ),
    ]
