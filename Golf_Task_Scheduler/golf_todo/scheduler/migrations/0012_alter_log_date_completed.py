# Generated by Django 3.2.2 on 2021-10-23 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scheduler', '0011_alter_log_date_completed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log',
            name='date_completed',
            field=models.DateField(default='2001-01-01'),
        ),
    ]
