from django.db import models
from django.contrib.auth.models import User
#from login.models import User as Profile

#model that records transactions 
#recipe and amount served 

class Mealmade(models.Model):
	recipename = models.CharField(max_length=100,)
	amount = models.IntegerField()
	calories = models.IntegerField()
	person_of = models.ForeignKey(User,null=True,on_delete=models.CASCADE)

	def __str__(self):
		return self.recipename

