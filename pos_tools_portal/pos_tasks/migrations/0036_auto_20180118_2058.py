# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_tasks', '0035_auto_20180118_2056'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='parameter',
            options={'verbose_name': 'Task Parameter', 'verbose_name_plural': 'Task Parameters'},
        ),
    ]
