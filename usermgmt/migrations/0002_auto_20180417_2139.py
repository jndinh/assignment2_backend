# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-18 01:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usermgmt', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='timestamp',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
