# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_tasks', '0030_auto_20180110_0515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='executionresult',
            name='jenkins_build_number',
            field=models.CharField(default='0', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='executionresult',
            name='jenkins_job_name',
            field=models.CharField(default='None', max_length=240, null=True),
        ),
    ]
