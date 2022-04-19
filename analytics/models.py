from tkinter import CASCADE
from django.db import models
from login.models import UserAccount
from recipe.models import Recipe
from datetime import datetime

#model that records transactions 
#recipe and amount served 

""" class Mealmade(models.Model):
	recipename = models.ForeignKey(Recipe,null=True, on_delete=models.CASCADE)
	amount = models.IntegerField()
	date = models.DateField(default=datetime.now)
	person_of = models.ForeignKey(UserAccount,null=True,on_delete=models.CASCADE)

	def __str__(self):
		return self.recipename

 """