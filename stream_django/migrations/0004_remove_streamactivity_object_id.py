# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stream_django', '0003_auto_20160430_1041'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='streamactivity',
            name='object_id',
        ),
    ]
