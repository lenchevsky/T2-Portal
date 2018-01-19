# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_tasks', '0026_remove_simpletask_snow_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='snow_token',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='snow_url',
            field=models.URLField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='snow_user',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
