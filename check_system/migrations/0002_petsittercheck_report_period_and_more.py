# Generated by Django 5.0.2 on 2024-10-16 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('check_system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='petsittercheck',
            name='report_period',
            field=models.IntegerField(default=3),
        ),
        migrations.AddField(
            model_name='petsittercheck',
            name='start_time',
            field=models.TimeField(default='12:00:00'),
        ),
    ]