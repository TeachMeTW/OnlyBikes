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

###############################################################################################

oauth = OAuth()

oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )
    
def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("index")))

# 👆 We're continuing from the steps above. Append this to your webappexample/views.py file.

def logout(request):
    request.session.clear()

    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )


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

    print(message.sid)

############################################################################################### 

def index(request):
    return

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
    
    bike = BikeModel.objects.create(brand = brand, model = model,price = price,condition = condition,location = location,description = description)
    bike.save()

    return HttpResponseRedirect(reverse('test_view'))