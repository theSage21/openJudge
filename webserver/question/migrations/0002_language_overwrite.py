# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('question', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='overwrite',
            field=models.BooleanField(help_text='overwrite required for storing the source code', default=False),
        ),
    ]
