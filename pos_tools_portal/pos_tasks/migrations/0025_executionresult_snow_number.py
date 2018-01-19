# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_tasks', '0024_simpletask_snow_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='executionresult',
            name='snow_number',
            field=models.CharField(default='INC00001', max_length=50),
            preserve_default=False,
        ),
    ]
