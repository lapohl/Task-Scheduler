# Generated by Django 3.2.2 on 2021-10-26 01:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0014_alter_log_date_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='date_completed',
            field=models.DateField(default=datetime.date(2022, 2, 3)),
        ),
    ]
