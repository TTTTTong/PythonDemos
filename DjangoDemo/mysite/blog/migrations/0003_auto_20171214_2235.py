# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-14 22:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20171214_2230'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='view',
            new_name='views',
        ),
    ]
