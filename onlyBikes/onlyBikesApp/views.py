from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import BikeModel
from django.template import loader
from django.urls import reverse

def index(request):
    bikes = BikeModel.objects.all()
    
    template = loader.get_template('onlyBikesApp/test_view.html')
    context = {
        'bikes' : bikes,
    }
    return HttpResponse(template.render(context, request), status = 200)

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