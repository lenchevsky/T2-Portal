# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_tasks', '0028_auto_20180110_0405'),
    ]

    operations = [
        migrations.AlterField(
            model_name='executionresult',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
