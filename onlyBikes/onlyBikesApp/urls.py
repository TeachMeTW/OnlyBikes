from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login, name="login"),
    path("logout", views.logout, name="logout"),
    path("callback", views.callback, name="callback"),
    path('add/', views.add, name='add'),
    path('add/addbike/', views.addbike, name='addbike'),
]
