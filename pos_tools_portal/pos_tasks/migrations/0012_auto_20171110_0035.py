# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-10 00:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pos_tasks', '0011_auto_20171109_2359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='results',
        ),
        migrations.AddField(
            model_name='executionresult',
            name='task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='pos_tasks.Task'),
        ),
    ]
