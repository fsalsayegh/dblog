# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-14 14:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posta', '0004_fatmaa_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fatmaa',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
