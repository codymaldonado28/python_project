# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2019-11-15 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_registration_app', '0003_trip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='end_date',
            field=models.DateField(null=True),
        ),
    ]
