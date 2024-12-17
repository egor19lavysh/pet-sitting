# Generated by Django 5.0.2 on 2024-12-17 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('check_system', '0008_report_analysis'),
    ]

    operations = [
        migrations.AddField(
            model_name='petsittercheck',
            name='status',
            field=models.CharField(choices=[('IN PROCESS', 'IN PROCESS'), ('SUCCESS', 'SUCCESS'), ('FAILURE', 'FAILURE')], default='SUCCESS', max_length=255),
        ),
    ]
