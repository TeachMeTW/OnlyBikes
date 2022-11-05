from django.db import models

# Create your models here.
class BikeModel(models.Model):
    
    location = models.CharField(max_length = 200)
    price = models.IntegerField()
    model = models.CharField(max_length = 200)
    brand = models.CharField(max_length = 100)
    description = models.CharField(max_length = 500)
    
    COND = (
        ('N', 'New'),
        ('LN', 'Like-New'),
        ('U', 'Used'),
    )
    condition = models.CharField(max_length = 2, choices = COND)
    