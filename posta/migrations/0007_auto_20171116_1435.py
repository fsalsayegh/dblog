# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 14:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posta', '0006_fatmaa_auther'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fatmaa',
            old_name='auther',
            new_name='author',
        ),
    ]
