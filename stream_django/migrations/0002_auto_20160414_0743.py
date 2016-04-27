# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stream_django', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamactivity',
            name='activity_actor_id',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='streamactivity',
            name='activity_author_feed',
            field=models.CharField(max_length=100, blank=True, null=True),
        ),
    ]
