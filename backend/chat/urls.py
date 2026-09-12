from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('alan/olustur/', MesajlasmaAlaniOlusturView.as_view(), name='alan-olustur'),
    path('mesaj/olustur/', MesajOlusturView.as_view(), name='mesaj-olustur'),
    path('mesaj/listele/<int:mesajlasma_alani_id>/', MesajListView.as_view(), name='mesaj-listele'),
    path('alan/kontrol/<int:satici_id>/', OdaKontrolView.as_view(), name='alan-kontrol'),
    path('alan/kontrol/satici/', OdaKontrolSaticiView.as_view(), name='alan-satici-kontrol')
]