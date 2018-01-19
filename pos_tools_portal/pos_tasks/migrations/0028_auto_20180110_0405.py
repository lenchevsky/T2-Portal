# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_tasks', '0027_auto_20180110_0223'),
    ]

    operations = [
        migrations.AlterField(
            model_name='executionresult',
            name='output',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='executionresult',
            name='snow_number',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='executionresult',
            name='user_signature',
            field=models.CharField(default='System', max_length=250),
        ),
    ]
