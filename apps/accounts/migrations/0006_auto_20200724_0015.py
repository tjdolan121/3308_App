# Generated by Django 3.0.7 on 2020-07-24 00:15

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20200724_0013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customaccount',
            name='eButton_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 7, 24, 0, 12, 49, 404577, tzinfo=utc)),
        ),
    ]
