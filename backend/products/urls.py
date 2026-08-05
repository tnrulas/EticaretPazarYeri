from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('Urunliste/', ProductListView.as_view(), name='urun-liste'),
    path('Urunliste/<int:pk>/', ProductDetailView.as_view(), name='urun-detay'),
    path('Urunekle/', ProductCreateView.as_view(), name='urun-ekle'),
]
