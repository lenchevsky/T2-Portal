# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-09 05:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pos_tasks', '0008_task_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos_tasks.Project'),
        ),
    ]