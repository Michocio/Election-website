# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-23 11:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PKW', '0005_auto_20160521_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gmina',
            name='czas',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
