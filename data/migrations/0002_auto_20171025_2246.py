# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 14:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result01',
            name='eventLevel',
            field=models.CharField(max_length=20),
        ),
    ]
