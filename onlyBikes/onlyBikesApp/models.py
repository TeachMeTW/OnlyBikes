from django.db import models
from django.contrib.auth.models import AbstractUser

COND = (
        ('N', 'New'),
        ('LN', 'Like-New'),
        ('U', 'Used'),
    )

# Create your models here.
class BikeModel(models.Model):
    
    image_dir = models.ImageField(upload_to='upload/', default='/bicycle-pictogram.png')
    image_url = models.CharField(max_length = 200, default="", blank=True)
    location = models.CharField(max_length = 200, default = "", blank=True)
    price = models.IntegerField(default = 0, blank=True)
    model = models.CharField(max_length = 200, default = "", blank=True)
    brand = models.CharField(max_length = 100, default = "", blank=True)
    description = models.CharField(max_length = 500, default = "", blank=True)
    startRental = models.DateTimeField(default='2002-06-05',blank=True)
    endRental = models.DateTimeField(default='2002-06-05', blank=True)
    beingRented = models.BooleanField(default = False, blank=True)
    condition = models.CharField(max_length = 2, choices = COND, default = "U", blank=True)
    original_owner = models.CharField(max_length = 200, default="rescued", blank=True)
    location_rescued = models.CharField(max_length = 200, default="", blank=True)

class User(AbstractUser):
    
    profile_image = models.ImageField(default ='/default.png')
    bio = models.CharField(max_length=1000)
    bikes = models.ManyToManyField(BikeModel, blank=True)
    phone_number = models.CharField(max_length=10)
    REQUIRED_FIELDS = ['email', 'password']
    pass
    

    




