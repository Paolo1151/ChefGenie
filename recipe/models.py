from django.db import models
from login.models import UserAccount
from datetime import datetime

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    unit = models.CharField(max_length=10)
    calories = models.FloatField()
    category = models.CharField(max_length=100, default="")

class Recipe(models.Model):
    name = models.CharField(max_length=150)
    tags = models.CharField(max_length=255)
    ingredients = models.ManyToManyField(Ingredient, through='Requirement')
    steps = models.TextField(default='1. Prepare ingredients. | 2. Cook food. | 3. Serve food.')

    def __str__(self):
        return self.name

class Requirement(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='recipe')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='ingredient')
    required_amount = models.FloatField()

class RecipeReview(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    rating = models.FloatField()
    comment = models.CharField(max_length=250, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Mealmade(models.Model):
	recipe = models.ForeignKey(Recipe,null=True, on_delete=models.CASCADE)
	amount = models.FloatField()
	date = models.DateField(default=datetime.now)
	user = models.ForeignKey(UserAccount,null=True,on_delete=models.CASCADE)