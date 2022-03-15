from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=150)
    tags = models.CharField(max_length=255)