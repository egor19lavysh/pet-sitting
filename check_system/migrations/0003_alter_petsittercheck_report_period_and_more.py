# Generated by Django 5.0.2 on 2024-10-16 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('check_system', '0002_petsittercheck_report_period_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='petsittercheck',
            name='report_period',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='petsittercheck',
            name='start_time',
            field=models.TimeField(default='12:00'),
        ),
    ]