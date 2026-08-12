from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/kayit/satici', CreateCustomSellerUserView.as_view(), name='kullanici-satici-kayit'),
    path('auth/kayit/musteri', CreateCustomBuyerUserView.as_view(), name='kullanici-musteri-kayit'),
    path('auth/giris/', CustomLoginView.as_view(), name='kullanici-giris'),
    path('auth/yenile/', TokenRefreshView.as_view(), name='token-yenile'),
]
