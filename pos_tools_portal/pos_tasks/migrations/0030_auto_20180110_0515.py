# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_tasks', '0029_auto_20180110_0445'),
    ]

    operations = [
        migrations.AlterField(
            model_name='executionresult',
            name='task',
            field=models.ForeignKey(to='pos_tasks.SimpleTask', null=True),
        ),
    ]
