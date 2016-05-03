# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stream_django', '0004_remove_streamactivity_object_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamactivity',
            name='object_pk',
            field=models.TextField(blank=True, null=True),
        ),
    ]
