# Generated by Django 5.1.4 on 2024-12-22 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_remove_order_need_sitting_remove_order_need_walking_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='weight',
            field=models.CharField(choices=[('Легкий (до 5 кг)', 'Легкий (до 5 кг)'), ('Средний (до 15 кг)', 'Средний (до 15 кг)'), ('Тяжелый (больше 15 кг)', 'Тяжелый (больше 15 кг)')], max_length=255),
        ),
    ]