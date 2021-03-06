# Generated by Django 4.0.3 on 2022-04-18 14:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
        ('recipe', '0004_recipereview'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mealmade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('date', models.DateField(default=datetime.datetime.now)),
                ('person_of', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='login.useraccount')),
                ('recipename', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recipe.recipe')),
            ],
        ),
    ]
