# Generated by Django 4.0.3 on 2022-04-04 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0004_alter_user_height_alter_user_weight_and_more'),
        ('recipe', '0003_ingredient_requirement_recipe_ingredients'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('comment', models.CharField(blank=True, max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.recipe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.user')),
            ],
        ),
    ]
