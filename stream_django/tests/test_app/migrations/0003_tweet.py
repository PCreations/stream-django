# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import stream_django.activity


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0002_auto_20141119_0647'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tweet',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
            ],
            bases=(stream_django.activity.Activity, models.Model),
        ),
    ]
