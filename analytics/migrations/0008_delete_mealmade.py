# Generated by Django 4.0.3 on 2022-04-18 14:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0007_remove_mealmade_calories_mealmade_date_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Mealmade',
        ),
    ]
