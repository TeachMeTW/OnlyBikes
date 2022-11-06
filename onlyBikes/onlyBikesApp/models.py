from django.db import models
from django.contrib.auth.models import AbstractUser

COND = (
        ('N', 'New'),
        ('LN', 'Like-New'),
        ('U', 'Used'),
    )

# Create your models here.
class BikeModel(models.Model):
    
    image = models.ImageField(upload_to='upload/', default="", blank=True)
    image_url = models.CharField(max_length = 200, default="", blank=True)
    location = models.CharField(max_length = 200, default="", blank=True)
    price = models.IntegerField(default=0, blank=True)
    model = models.CharField(max_length = 200, default="", blank=True)
    brand = models.CharField(max_length = 100, default="", blank=True)
    description = models.CharField(max_length = 500, blank=True)
    startRental = models.DateTimeField(default='2002-06-05',blank=True)
    endRental = models.DateTimeField(default='2002-06-05',blank=True)
    beingRented = models.BooleanField(default = False, blank=True)
    condition = models.CharField(max_length = 2, choices = COND, default="U", blank=True)
    original_owner = models.CharField(max_length = 200, default="rescued", blank=True)
    rescued_long = models.FloatField(default=0, blank=True)
    rescued_lat = models.FloatField(default=0, blank=True)


class User(AbstractUser):
    
    profile_image = models.ImageField(default ='/default.png', blank=True)
    bio = models.CharField(max_length=1000, default="", blank=True)
    bikes = models.ManyToManyField(BikeModel, blank=True)
    phone_number = models.CharField(max_length=10, default="", blank=True)
    REQUIRED_FIELDS = ['email', 'password']
    pass
    

    




