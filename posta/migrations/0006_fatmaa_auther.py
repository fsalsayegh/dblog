# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-15 17:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('posta', '0005_auto_20171114_1445'),
    ]

    operations = [
        migrations.AddField(
            model_name='fatmaa',
            name='auther',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]