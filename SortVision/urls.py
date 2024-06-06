from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('main', views.main, name='main'),
    path('lista/', views.lista, name='lista'),
    path('losuj_polfinaly/', views.losuj_polfinaly, name='losuj_polfinaly'),
    path('polfinaly/', views.polfinal, name='polfinal'),
    path('polfinal/<int:polfinal_num>/', views.polfinal_detail, name='polfinal_detail'),
    path('zapisz_polfinaly/', views.zapisz_polfinaly, name='zapisz_polfinaly'),
    path('potwierdzenie_polfinaly/', views.potwierdzenie_polfinaly, name='potwierdzenie_polfinaly'),
    path('final', views.final, name='final'),
    path('lista/new/', views.kraj_new, name='kraj_new'),
    path('lista/<int:pk>/', views.lista_detail, name='lista_detail'),

]