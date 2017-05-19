# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('violations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('who_id', models.IntegerField()),
                ('who_meta', models.TextField(max_length=2000)),
                ('what', models.CharField(max_length=50, null=True, verbose_name=b'What', blank=True)),
                ('what_meta', models.TextField(max_length=2000)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('violation', models.ForeignKey(related_name='actions', default=None, blank=True, to='violations.Violation', null=True)),
            ],
        ),
    ]
