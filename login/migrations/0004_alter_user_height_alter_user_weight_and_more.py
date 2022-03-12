# Generated by Django 4.0.3 on 2022-03-09 09:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0003_remove_user_featured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='height',
            field=models.DecimalField(decimal_places=2, default=160.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='user',
            name='weight',
            field=models.DecimalField(decimal_places=2, default=60.0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='user',
            name='weight_goal',
            field=models.DecimalField(decimal_places=2, default=60.0, max_digits=5),
        ),
    ]
