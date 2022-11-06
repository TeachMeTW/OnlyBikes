from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class BikeModel(models.Model):
    
    image = models.ImageField(upload_to='upload/')
    location = models.CharField(max_length = 200)
    price = models.IntegerField()
    model = models.CharField(max_length = 200)
    brand = models.CharField(max_length = 100)
    description = models.CharField(max_length = 500)
    startRental = models.DateTimeField(default='2002-06-05')
    endRental = models.DateTimeField(default='2002-06-05')
    beingRented = models.BooleanField(default = False)
    
    
    COND = (
        ('N', 'New'),
        ('LN', 'Like-New'),
        ('U', 'Used'),
    )
    condition = models.CharField(max_length = 2, choices = COND)

class User(AbstractUser):
    
    profile_image = models.ImageField()
    bio = models.CharField(max_length=1000)
    bikes = models.ManyToManyField(BikeModel, blank=True)
    phone_number = models.CharField(max_length=10)
    REQUIRED_FIELDS = ['email', 'password']
    pass
    

    




