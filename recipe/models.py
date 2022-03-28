from django.db import models

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)

class Recipe(models.Model):
    name = models.CharField(max_length=150)
    tags = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient, through='Requirement')
    steps = models.TextField(default='1. Prepare ingredients. | 2. Cook food. | 3. Serve food.')

class Requirement(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredient')
    required_amount = models.FloatField()