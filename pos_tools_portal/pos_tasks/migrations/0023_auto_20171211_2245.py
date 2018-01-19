# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos_tasks', '0022_auto_20171113_0601'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='header',
            options={'verbose_name': 'Task Header', 'verbose_name_plural': 'Task Headers'},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'verbose_name': 'POS Project', 'verbose_name_plural': 'POS Projects'},
        ),
        migrations.AlterModelOptions(
            name='resttask',
            options={'verbose_name': 'REST Call Task', 'verbose_name_plural': 'REST Call Tasks'},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'verbose_name': 'Jenkins Task', 'verbose_name_plural': 'Jenkins Tasks'},
        ),
        migrations.AddField(
            model_name='project',
            name='hipchat_room',
            field=models.IntegerField(default=398),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='hipchat_token',
            field=models.CharField(default='TO3jofkCrsbrx2nyddsKfUB6So4ksToMifSkauaw', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='hipchat_url',
            field=models.URLField(default='https://hipchat.cantire.com', max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='simpletask',
            name='project',
            field=models.ForeignKey(to='pos_tasks.Project', on_delete=None),
        ),
    ]
