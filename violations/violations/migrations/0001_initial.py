# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.postgres.fields


class Migration(migrations.Migration):

    dependencies = [
        ('types_vio', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Violation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vio_date', models.DateTimeField(auto_now_add=True)),
                ('who_id', models.IntegerField()),
                ('who_type', models.CharField(max_length=50, null=True, verbose_name=b'Who Type', blank=True)),
                ('who_meta', models.TextField(max_length=2000)),
                ('whom_id', models.IntegerField()),
                ('whom_type', models.CharField(max_length=50, null=True, verbose_name=b'Whom Type', blank=True)),
                ('whom_meta', models.TextField(max_length=2000)),
                ('cc_list', django.contrib.postgres.fields.ArrayField(size=None, base_field=models.IntegerField(), blank=True)),
                ('cc_list_meta', django.contrib.postgres.fields.ArrayField(size=None, base_field=models.TextField(max_length=2000), blank=True)),
                ('bcc_list', django.contrib.postgres.fields.ArrayField(size=None, base_field=models.IntegerField(), blank=True)),
                ('bcc_list_meta', django.contrib.postgres.fields.ArrayField(size=None, base_field=models.TextField(max_length=2000), blank=True)),
                ('status', models.CharField(max_length=50, null=True, verbose_name=b'Status', blank=True)),
                ('violation_nature', models.CharField(max_length=50, null=True, verbose_name=b'Violation Nature', blank=True)),
                ('vio_type', models.ForeignKey(default=None, blank=True, to='types_vio.Type', null=True)),
            ],
        ),
    ]
