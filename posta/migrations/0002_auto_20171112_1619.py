# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-12 16:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posta', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fatmaa',
            options={'ordering': ['title']},
        ),
        migrations.AddField(
            model_name='fatmaa',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
