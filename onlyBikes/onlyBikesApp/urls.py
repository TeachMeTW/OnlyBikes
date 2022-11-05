from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='test_view'),
    path('add/', views.add, name='add'),
    path('add/addbike/', views.addbike, name='addbike'),
]
