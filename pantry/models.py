from django.db import models

# Create your models here.
class Ingredients(models.Model):
	img = models.ImageField(upload_to='media/')
	name = models.CharField(max_length=100)
	amount = models.IntegerField()

