from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import BikeModel
from django.template import loader
from django.urls import reverse
import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render, redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
from twilio.rest import Client
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required 
from . models import User
###############################################################################################

test_bikes = [{
    "user" : "Sally May", 
    "brand" : "Co-op Cycles",
    "model" : "CTY 1.1",
    "price" : 20,
    "condition" : "New",
    "location" : "San Fransisco, CA",
    "image" : "https://i.ebayimg.com/images/g/hnsAAOSwalxhLRn6/s-l500.jpg",
    "description" : "Made for urban cruising. This bike features a low crossbar for easy mounts and dismounts, a flat handlebar for a heads-up ride and a versatile 3x8 drivetrain.",
},{
    "user" : "Robin Shultz",
    "brand" : "Schwinn",
    "model" : "Coston DX",
    "price" : 35,
    "condition" : "Used",
    "location" : "Santa Clara, CA",
    "image" : "https://cloudfront-us-east-1.images.arcpublishing.com/octane/6S2OXJZGXRCWXOZC4RALKFJFQU.jpg",
    "description" : "Schwinn is a brilliant choice as it features both pedal assist and throttle options. We also like that it has integrated lights (helpful when you’re biking home in the dark) and fenders (great for keeping mud off your work clothes on rainy days",
},{
    "user" : "Matthew Jew",
    "brand" : "Cervelo",
    "model" : "Caledonia Ultegra",
    "price" : 25,
    "condition" : "Like New",
    "location" : "New York, NY",
    "image" : "https://cyclingtips.com/wp-content/uploads/2021/01/2021-Cervelo-Caledonia-Ultegra-Di2-road-bike-review-cyclingtips-Field-test-4.jpg",
    "description" : "When you’re ready to move beyond casual rides and start training for distance and speed on pavement, a road bike will be the best fit.",
}, {
    "user" : "Shizuka Nigiyaka",
    "brand" : "VanMoof",
    "model" : "S3",
    "price" : 28,
    "condition" : "Used",
    "location" : "Compton, CA",
    "image" : "https://cdn.pocket-lint.com/r/s/970x/assets/images/152686-fitness-trackers-review-s3-vanmoof-2nd-set-image1-hden5uz0i9.jpg",
    "description" : "VanMoof has fostered something of a following amongst gear heads, and that approval is quickly extending to casual riders too. Sleek and stylish, the S3 e-bike boasts four speed settings, making hills nearly as easy as straightaways.",
},{
    "user" : "Lovemore Dumi",
    "brand" : "Ibis",
    "model" : "Hakka MX Disc 650b",
    "price" : 19,
    "condition" : "New",
    "location" : "Pasadena, CA",
    "image" : "https://www.cxmagazine.com/wp-content/uploads/2018/09/ibis-hakka-mx-cyclocross-gravel-IMG_8448-HDR-cxmagazine-ay_1.jpg",
    "description" : "VanMoof has fostered something of a following amongst gear heads, and that approval is quickly extending to casual riders too. Sleek and stylish, the S3 e-bike boasts four speed settings, making hills nearly as easy as straightaways.",
},{
    "user" : "Efe Aamina",
    "brand" : "Liv",
    "model" : "Alight 2 Disc",
    "price" : 21,
    "condition" : "New",
    "location" : "Condard, CA",
    "image" : "https://s3.amazonaws.com/www.bikerumor.com/wp-content/uploads/2021/11/23191628/showcase7.jpg",
    "description" : "It comes equipped with reliable Shimano components and accessory mounts so you can add fenders, racks or a kickstand depending on whether you use your bike for grocery runs or commuting during the rainy season.",
},{
    "user" : "Oni Ochieng",
    "brand" : "Lectric",
    "model" : "XP Step-Thru 2.0",
    "price" : 25,
    "condition" : "Used",
    "location" : "Condard, CA",
    "image" : "https://cleantechnica.com/files/2021/05/2021.05-lectric-xp-step-thru-cargo-baskets-accessories-ebike-electric-bicycle-KYLE3.jpg",
    "description" : "With high-quality brakes and pedal assist, the XP Step-Thru 2.0 is ideal for commuting and everyday riding. While some folding bikes feel unstable because of their small tires, the long wheel base of this model adds stability and finesse to your ride.",
},
]

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
    bike_list = []
    for bike_obj in test_bikes:
        bike = BikeModel.objects.create(
            brand = bike_obj["brand"], 
            model = bike_obj["model"], 
            price = bike_obj["price"], 
            condition = bike_obj["condition"], 
            location = bike_obj["location"], 
            description = bike_obj["description"],
            image_url = bike_obj["image"],
            original_owner = bike_obj["user"]
            )
        bike_list.append(bike)
    return render(request, "index.html", {"bike_list" : bike_list})

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

def home(request):
    return render(request, 'home.html')

def temp(request):
    return render(request, 'temp.html')

def show(request):
    return render(request, 'show.html')

def contact(request):
    return render(request, 'contact.html')

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
    print(request.POST)
    user.first_name = first
    print(user.last_name, last)
    user.last_name = last
    user.email = email
    user.phone_number = phone
    print(user.bio, bio)
    user.bio = bio
    user.save()
    return HttpResponseRedirect(reverse('profile'))
