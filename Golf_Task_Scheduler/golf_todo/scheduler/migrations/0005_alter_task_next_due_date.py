# Generated by Django 3.2.2 on 2021-06-06 00:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0004_auto_20210605_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='next_due_date',
            field=models.DateField(default=datetime.date(2021, 6, 6)),
        ),
    ]
