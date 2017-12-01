# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-10 21:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pos_tasks', '0017_auto_20171110_2140'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='active',
        ),
        migrations.RemoveField(
            model_name='task',
            name='description',
        ),
        migrations.RemoveField(
            model_name='task',
            name='id',
        ),
        migrations.RemoveField(
            model_name='task',
            name='name',
        ),
        migrations.RemoveField(
            model_name='task',
            name='parameters',
        ),
        migrations.AddField(
            model_name='task',
            name='simpletask_ptr',
            field=models.OneToOneField(auto_created=True, default=1, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='pos_tasks.SimpleTask'),
            preserve_default=False,
        ),
    ]