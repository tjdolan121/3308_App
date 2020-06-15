# Generated by Django 3.0.7 on 2020-06-15 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200611_0026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customaccount',
            name='email',
            field=models.EmailField(max_length=255, unique=True, verbose_name='email address'),
        ),
    ]
