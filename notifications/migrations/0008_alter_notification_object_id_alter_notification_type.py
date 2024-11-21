# Generated by Django 5.0.2 on 2024-11-07 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0007_rename_system_id_notification_object_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='object_id',
            field=models.IntegerField(blank=True, default=-1),
        ),
        migrations.AlterField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('report_load', 'report_load'), ('report_watch', 'report_watch'), ('order_created', 'order_created'), ('order_status', 'order_status'), ('other', 'other')], max_length=255),
        ),
    ]