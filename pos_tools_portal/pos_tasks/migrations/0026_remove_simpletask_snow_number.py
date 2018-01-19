# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_tasks', '0025_executionresult_snow_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='simpletask',
            name='snow_number',
        ),
    ]
