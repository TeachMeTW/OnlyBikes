from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('temp/', views.temp, name='temp'),
    path('show/', views.show, name='show'),
    path('logout/', views.logout, name ='logout'),
    path('', views.home, name='home'),

    # REMOVE THIS
]
