# Generated by Django 4.0.3 on 2022-03-29 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_remove_mealmade_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mealmade',
            name='calories',
            field=models.IntegerField(),
        ),
    ]