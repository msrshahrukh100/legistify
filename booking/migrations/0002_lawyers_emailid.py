# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-04-24 07:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lawyers',
            name='emailid',
            field=models.EmailField(default='abc@abc.com', max_length=50),
        ),
    ]
