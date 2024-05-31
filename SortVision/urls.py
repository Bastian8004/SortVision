from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('lista', views.lista, name='list'),
    path('polfinal', views.polfinal),
    path('final', views.final, name='Final'),

]