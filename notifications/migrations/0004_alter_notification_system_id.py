# Generated by Django 5.0.2 on 2024-10-29 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0003_remove_notification_url_notification_system_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='system_id',
            field=models.IntegerField(default=-1),
        ),
    ]
