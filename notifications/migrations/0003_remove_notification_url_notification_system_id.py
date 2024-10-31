# Generated by Django 5.0.2 on 2024-10-29 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_notification_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='url',
        ),
        migrations.AddField(
            model_name='notification',
            name='system_id',
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]