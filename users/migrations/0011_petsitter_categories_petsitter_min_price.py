# Generated by Django 5.0.2 on 2024-11-21 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pet', '0003_alter_pet_photo'),
        ('users', '0010_remove_user_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='petsitter',
            name='categories',
            field=models.ManyToManyField(to='pet.category'),
        ),
        migrations.AddField(
            model_name='petsitter',
            name='min_price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=7),
        ),
    ]