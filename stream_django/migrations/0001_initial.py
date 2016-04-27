# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StreamActivity',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('actor', models.CharField(blank=True, max_length=100, null=True)),
                ('verb', models.CharField(blank=True, max_length=100, null=True)),
                ('original_foreign_id', models.CharField(blank=True, max_length=100, null=True)),
                ('_data', models.TextField(default='', db_column='data')),
            ],
        ),
    ]
