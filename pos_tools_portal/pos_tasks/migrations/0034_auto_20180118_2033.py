# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_tasks', '0033_auto_20180118_2025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='environment',
            options={'verbose_name': 'Environment', 'verbose_name_plural': 'Environments'},
        ),
    ]
