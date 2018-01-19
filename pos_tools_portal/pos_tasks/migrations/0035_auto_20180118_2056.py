# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_tasks', '0034_auto_20180118_2033'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='resttask',
            options={'verbose_name': 'REST Task', 'verbose_name_plural': 'REST Tasks'},
        ),
    ]
