# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.utils.timezone
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('infile', models.FileField(upload_to='test_cases')),
                ('outfile', models.FileField(upload_to='test_cases')),
                ('sample_code', models.FileField(upload_to='solutions')),
            ],
        ),
        migrations.CreateModel(
            name='AnswerType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('details', models.TextField()),
                ('wrapper', models.FileField(upload_to='wrappers')),
                ('overwrite', models.BooleanField(default=False, help_text='overwrite required for storing the source code')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user_ptr', models.OneToOneField(parent_link=True, serialize=False, auto_created=True, primary_key=True, to=settings.AUTH_USER_MODEL)),
                ('score', models.FloatField(default=0.0)),
                ('last_solved', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('qno', models.IntegerField()),
                ('title', models.CharField(max_length=50)),
                ('text', models.TextField(default='Question text goes here')),
            ],
        ),
        migrations.AddField(
            model_name='attempt',
            name='language',
            field=models.ForeignKey(related_name='language', to='question.Language'),
        ),
        migrations.AddField(
            model_name='attempt',
            name='player',
            field=models.ForeignKey(related_name='player', to='question.Profile'),
        ),
        migrations.AddField(
            model_name='attempt',
            name='question',
            field=models.ForeignKey(related_name='question', to='question.Question'),
        ),
        migrations.AddField(
            model_name='answer',
            name='answer_type',
            field=models.ForeignKey(related_name='answer_type', to='question.AnswerType'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.OneToOneField(to='question.Question'),
        ),
    ]
