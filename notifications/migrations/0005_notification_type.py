# Generated by Django 5.0.2 on 2024-11-04 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0004_alter_notification_system_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('system', 'system'), ('order', 'order')], default='system', max_length=255),
        ),
    ]
