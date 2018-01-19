# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_tasks', '0032_auto_20180111_0213'),
    ]

    operations = [
        migrations.RenameModel('Project', 'Environment'),
        migrations.RenameField('SimpleTask', 'project', 'environment')
    ]
