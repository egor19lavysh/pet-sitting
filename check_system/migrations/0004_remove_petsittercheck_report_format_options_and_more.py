# Generated by Django 5.0.2 on 2024-10-16 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('check_system', '0003_alter_petsittercheck_report_period_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='petsittercheck',
            name='report_format_options',
        ),
        migrations.AddField(
            model_name='petsittercheck',
            name='report_format',
            field=models.CharField(choices=[('Текст', 'Текст'), ('Фотография', 'Фотография'), ('Видео', 'Видео')], default='Текст', max_length=15),
        ),
    ]
