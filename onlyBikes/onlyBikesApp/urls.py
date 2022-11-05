from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('temp/', views.temp, name='temp'),
    path('show/', views.show, name='show'),
    path('', views.home, name='home'),

    # REMOVE THIS
]
