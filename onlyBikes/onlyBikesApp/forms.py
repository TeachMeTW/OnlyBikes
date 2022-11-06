from django.forms import ModelForm
from .models import User, BikeModel

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'bio', 'phone_number', 'profile_image']