from django.db import models

# Create your models here.
class User(models.Model):
    email_address = models.EmailField()
    username = models.CharField(
        max_length=30
        )
    password = models.CharField(
        max_length=30
        )
    weight = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=60.00
        )
    height = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=160.00
        )
    weight_goal = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=60.00
        )
    calorie_goal = models.IntegerField(
        default=2500
        )

    @property
    def bmi(self):
        w = self.weight
        h = (self.height * self.height) / 10000
        return w / h