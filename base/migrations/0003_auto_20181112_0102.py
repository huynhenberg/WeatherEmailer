# Generated by Django 2.1.2 on 2018-11-12 01:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_auto_20181109_2024'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='activation_date',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='last_modified_datetime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
