from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('adres/ekle/', AddressCreateView.as_view(), name='adres-ekle'),
    path('adres/liste/', AddressListView.as_view(), name='adres-liste'),
    
    path('sepet/ekle/', CartItemCreateView.as_view(), name='sepet-ekle'),
    path('sepet/liste/', CartItemListView.as_view(), name='sepet-liste'),
    
    path('liste/', OrderListView.as_view(), name='siparis-liste'),
    path('olustur/', OrderCreateView.as_view(), name='siparis-ekle'),
]
