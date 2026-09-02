from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser
from .serializer import CreateCustomSellerUserSerializer,CreateCustomBuyerUserSerializer, ListMyAccountSerializer, ListSellerAccountSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import CustomTokenSerializer
from django.shortcuts import get_object_or_404


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

class ListMyAccountView(generics.RetrieveAPIView):
    serializer_class = ListMyAccountSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user

class ListSellerAccountView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ListSellerAccountSerializer
    permission_classes = [AllowAny]
    
    lookup_field = 'id'
    lookup_url_kwarg = 'seller_id'