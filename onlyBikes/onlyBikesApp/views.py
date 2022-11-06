from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import BikeModel
from django.template import loader
from django.urls import reverse
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render, redirect
from django.urls import reverse
from twilio.rest import Client
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required 
from . models import User
from .utils.utils import test_data
from os import environ
###############################################################################################


# Auth0 Section
oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.SOCIAL_AUTH_AUTH0_KEY,
    client_secret=settings.SOCIAL_AUTH_AUTH0_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.SOCIAL_AUTH_AUTH0_DOMAIN}/.well-known/openid-configuration",
)

def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )
    
def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("index")))


@login_required
def logout(request):
    django_logout(request)
    domain = settings.SOCIAL_AUTH_AUTH0_DOMAIN
    client_id = settings.SOCIAL_AUTH_AUTH0_KEY
    return_to = 'http://127.0.0.1:8000' # this can be current domain
    return redirect(f'https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}')


###############################################################################################    

# TWILIO CUSTOMIZATION

twilio_sid = settings.TWILIO_SID
twilio_auth = settings.TWILIO_AUTH
client = Client(twilio_sid,twilio_auth)

def testmessage():
    message = client.messages.create(
    body='ザワルドときをとまれ',
    from_='+18563866349',
    to='+18187978710'
    )

    # print(message.sid)

############################################################################################### 

# Everything Else

def index(request):

    all_bikes = BikeModel.objects.all()
    
    # Note: Remove this in production
    if len(all_bikes) < 7:
        all_bikes = test_data()
        for bike in all_bikes: 
            bike.save()

    return render(request, "index.html", {"all_bikes" : all_bikes})

def home(request):
    return render(request, 'home.html')

def temp(request):
    return render(request, 'temp.html')

def show(request, id):
    bike = BikeModel.objects.filter(id=id)

    if len(bike) == 0:
        return redirect('/index')
    return render(request, 'show.html', {"bike" : bike[0]})

def contact(request):
    return render(request, 'contact.html')

def leaderboard(request):
    all_bikes = BikeModel.objects.filter(original_owner="rescued") 
    print(all_bikes)
    return render(request, 'leaderboard.html', {
        "mapbox_token" : environ["MAPBOX_TOKEN"],
        "all_bikes" : all_bikes
        })

# -- Utility Functions --

def add(request):
    template = loader.get_template('onlyBikesApp/add.html')
    return HttpResponse(template.render({}, request))

def addbike(request):
    brand = request.POST['brand']
    model = request.POST['model']
    price = request.POST['price']
    condition = request.POST['condition']
    location = request.POST['location']
    description = request.POST['description']
    
    bike = BikeModel.objects.create(brand = brand, model = model, price = price, condition = condition, location = location, description = description)
    bike.save()

    return HttpResponseRedirect(reverse('test_view'))

    # return HttpResponse(html, status = 200)

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def update_profile(request):
    username = request.user
    first = request.POST['first']
    last = request.POST['last']
    email = request.POST['email']
    phone = request.POST['phone']
    bio = request.POST['bio']
    user = User.objects.get(username = username)
    # print(request.POST)
    user.first_name = first
    # print(user.last_name, last)
    user.last_name = last
    user.email = email
    user.phone_number = phone
    # print(user.bio, bio)
    user.bio = bio
    user.save()
    return HttpResponseRedirect(reverse('profile'))
