# Generated by Django 4.0.3 on 2022-04-06 18:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
        ('analytics', '0005_alter_mealmade_calories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mealmade',
            name='person_of',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='login.useraccount'),
        ),
    ]