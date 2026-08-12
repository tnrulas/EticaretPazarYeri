from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser
from .serializer import CreateCustomSellerUserSerializer,CreateCustomBuyerUserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import CustomTokenSerializer


# Create your views here.
class CreateCustomSellerUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateCustomSellerUserSerializer
    permission_classes = [AllowAny]

class CreateCustomBuyerUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CreateCustomBuyerUserSerializer
    permission_classes = [AllowAny]

class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenSerializer