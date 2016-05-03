# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('stream_django', '0002_auto_20160414_0743'),
    ]

    operations = [
        migrations.AddField(
            model_name='streamactivity',
            name='content_type',
            field=models.ForeignKey(blank=True, null=True, to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='streamactivity',
            name='object_id',
            field=models.TextField(blank=True, null=True),
        ),
    ]
