# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_tasks', '0023_auto_20171211_2245'),
    ]

    operations = [
        migrations.AddField(
            model_name='simpletask',
            name='snow_number',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
