# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shortcode', models.CharField(unique=True, max_length=50, verbose_name=b'ShortCode')),
                ('display', models.CharField(max_length=50, null=True, verbose_name=b'Display', blank=True)),
                ('severity', models.CharField(max_length=50, null=True, verbose_name=b'Severity', blank=True)),
                ('group', models.CharField(max_length=50, null=True, verbose_name=b'Group', blank=True)),
                ('configurable_counts', models.TextField(max_length=2000)),
            ],
        ),
    ]
