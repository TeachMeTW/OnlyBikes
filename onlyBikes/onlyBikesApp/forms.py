from django.forms import ModelForm
from .models import User, BikeModel

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'phone_number', 'profile_image']
        
class BikeForm(ModelForm):
    class Meta:
        model = BikeModel
        fields = ['image_dir', 'image_url', 'location', 'price', 'model', 'brand', 'description', 'startRental', 'endRental', 'beingRented', 'condition', 'original_owner', 'location_rescued']