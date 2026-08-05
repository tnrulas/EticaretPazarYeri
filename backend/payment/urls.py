from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('odeme/ekle/<int:order_id>/', PaymentCreateView.as_view(), name='odeme-ekle'),
    path('odeme/liste/', PaymentListView.as_view(), name='odeme-listele')
]