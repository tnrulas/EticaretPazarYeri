from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status

from accounts.models import CustomUser
from .models import Product
from .serializer import ProductSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import PermissionDenied

# Create your views here.
class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        
        if not self.request.user.is_seller:
            raise PermissionDenied("Only sellers can create products.")
        
        serializer.save(seller=self.request.user)

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    queryset = Product.objects.all()


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

