from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=150)
    tags = models.CharField(max_length=255)
    steps = models.TextField(default='1. Prepare ingredients. | 2. Cook food. | 3. Serve food.')