from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from .models import CustomUser
from products.models import Product
from .serializer import CreateCustomSellerUserSerializer,CreateCustomBuyerUserSerializer, ListMyAccountSerializer, ListSellerAccountSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import CustomTokenSerializer
from django.shortcuts import get_object_or_404
from products.serializer import ProductSerializer
from rest_framework.views import APIView


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

class ListFavoritesView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.request.user.favorites.all()

class ToggleFavoriteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        user = request.user
        
        if product in user.favorites.all():
            user.favorites.remove(product)
            return Response({"durum": False, "mesaj": "Favorilerden çıkarıldı"}, status=status.HTTP_200_OK)
        else:
            user.favorites.add(product)
            return Response({"durum": True, "mesaj": "Favorilere eklendi"}, status=status.HTTP_200_OK)