# Generated by Django 4.0.3 on 2022-03-13 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='static/pics')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.IntegerField()),
            ],
        ),
    ]
