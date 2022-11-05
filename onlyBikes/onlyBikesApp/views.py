from django.shortcuts import render
from django.http import HttpResponse
from .models import BikeModel

def index(request):
    bikes = BikeModel.objects.all()
    
    html = ''
    for b in bikes:
        var = f'<li> ({b.get_condition_display()}) {b.brand_name} {b.model_name} only: ${b.price}!! </li><br>'
        html = html + var
    return HttpResponse(html, status = 200)
