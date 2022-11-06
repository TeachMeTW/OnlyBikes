from django.forms import ModelForm
from . models import User, BikeModel

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['profile_image', 'bio', 'phone_number', 'email', 'password', 'first_name', 'last_name']
        
class BikeForm(ModelForm):
    class Meta:
        model = BikeModel
        fields = ['image_url', 'location', 'price', 'model', 'brand', 'description', 'startRental', 'endRental', 'beingRented', 'condition', 'original_owner', 'image', 'rescued_long', 'rescued_lat']