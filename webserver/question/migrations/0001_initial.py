# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('infile', models.FileField(upload_to='test_cases')),
                ('outfile', models.FileField(upload_to='test_cases')),
                ('sample_code', models.FileField(upload_to='solutions')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('source', models.FileField(upload_to='%t/')),
                ('correct', models.NullBooleanField(default=None)),
                ('stamp', models.DateTimeField(auto_now_add=True)),
                ('marks', models.FloatField()),
                ('remarks', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('details', models.TextField()),
                ('wrapper', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, to=settings.AUTH_USER_MODEL, auto_created=True, primary_key=True, serialize=False)),
                ('score', models.FloatField(default=0.0)),
                ('last_solved', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'user',
                'abstract': False,
                'verbose_name_plural': 'users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('qno', models.IntegerField()),
                ('title', models.CharField(max_length=50)),
                ('text', models.TextField(default='Question text goes here')),
            ],
        ),
        migrations.AddField(
            model_name='attempt',
            name='language',
            field=models.ForeignKey(to='question.Language', related_name='language'),
        ),
        migrations.AddField(
            model_name='attempt',
            name='player',
            field=models.ForeignKey(to='question.Profile', related_name='player'),
        ),
        migrations.AddField(
            model_name='attempt',
            name='question',
            field=models.ForeignKey(to='question.Question', related_name='question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='answer_type',
            field=models.ForeignKey(to='question.AnswerType', related_name='answer_type'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.OneToOneField(to='question.Question'),
        ),
    ]
