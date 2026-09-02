from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status

from accounts.models import CustomUser
from .models import Product, Review, ImageProduct
from .serializer import ProductSerializer, ProductReviewSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from orders.models import OrderItem

# Create your views here.
class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        
        if not self.request.user.is_seller:
            raise PermissionDenied("Only sellers can create products.")
        
        product = serializer.save(seller=self.request.user)
        
        ekstra_resimler = self.request.FILES.getlist('images')
        
        for resim in ekstra_resimler:
            ImageProduct.objects.create(image=resim, product=product)

class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    
class ProductCategoryListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        searched_category = self.request.query_params.get('category')
        
        if searched_category:
            
            return Product.objects.filter(category=searched_category) 
        
        return Product.objects.all()

class ProductSearchFilterView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    def get_queryset(self):
        
        searched_sentence = self.request.query_params.get('q', '')
        
        if searched_sentence:
            
            return Product.objects.filter(name__icontains=searched_sentence) 
        
        return Product.objects.none()


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class SellerProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        
        satici_id = self.kwargs.get('seller_id')
        
        return Product.objects.filter(seller=satici_id)
    


class ProductReviewView(generics.ListCreateAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes =  [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        
        return Review.objects.filter(product_id=product_id).order_by('-created_at')
    
    def perform_create(self, serializer):
        
        product_id = self.kwargs.get('product_id')
        product = get_object_or_404(Product, id=product_id)
        user = self.request.user
        
        is_bought = OrderItem.objects.filter(
            order__buyer=user,
            order__is_verified=True,
            product=product
        ).exists()
        
        if not is_bought:
            raise PermissionDenied("Sadece bu ürünü satın alan kullanıcılar yorum yapabilir.")
        
        serializer.save(user=user, product=product, is_buyed=is_bought)