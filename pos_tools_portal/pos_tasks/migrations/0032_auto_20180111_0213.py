# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_tasks', '0031_auto_20180110_0528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parameter',
            name='param_type',
            field=models.CharField(default='DEFAULT', max_length=20, choices=[('DEFAULT', 'Default Parameter'), ('URL', 'URL Parameter'), ('HEADER', 'Header Parameter')]),
        ),
    ]
