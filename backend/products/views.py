from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status

from accounts.models import CustomUser
from .models import Product, Review, ImageProduct, Category, CategoryAttribute, ProductValue
from .serializer import ProductSerializer, ProductReviewSerializer, CategorySerializer, ProductValueSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from orders.models import OrderItem
import json
from rest_framework.exceptions import ValidationError
from django.db.models import Q

# Create your views here.

class CategoryTreeListView(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        return Category.objects.filter(parent__isnull=True)
    
class CategoryProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        category_id = self.request.query_params.get('category')
        if not category_id:
            return Product.objects.none()
        
        category = Category.objects.filter(id=category_id).first()
        if not category:
            return Product.objects.none()
        
        ids = []
        stack = [category]
        while stack:
            current = stack.pop()
            ids.append(current.id)
            stack.extend(current.subcategories.all())

        return Product.objects.filter(category_id__in=ids)


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
        
        dinamik_ozellikler_str = self.request.data.get('dinamik_ozellikler')
        
        if dinamik_ozellikler_str:
            try:
                ozellikler_dict = json.loads(dinamik_ozellikler_str)
                
                for attr_id, value in ozellikler_dict.items():
                    if value and str(value).strip():
                        attribute = get_object_or_404(CategoryAttribute, id=attr_id)
                        ProductValue.objects.create(
                            product=product,
                            attribute=attribute,
                            value=value
                        )
            except json.JSONDecodeError:
                raise ValidationError("dinamik_ozellikler JSON formatında olmalıdır.")

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

class ProductSuggestionView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        
        product_id = self.kwargs.get('product_id')
        try:
            
            current_product = Product.objects.get(id=product_id)
            
            return Product.objects.filter(
                category=current_product.category
                ).exclude(
                    id=product_id
                ).order_by('?')[:5]
        except Product.DoesNotExist:
            return Product.objects.none()

class ProductFilterView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    
    GENEL_ALANLAR = [
        'is_bulk_sale', 'is_gift_wrap', 'has_video',
        'is_campaign', 'is_buy_together', 'is_buy_more_pay_less',
        'is_corporate_invoice', 'is_editor_choice'
    ]
    
    def get_queryset(self):
        genel = self.request.query_params.getlist('genel')
        ozel = self.request.query_params.getlist('ozel')
        category_id = self.request.query_params.get('category')
        q = self.request.query_params.get('q', '')

        if category_id:
            category = Category.objects.filter(id=category_id).first()
            if not category:
                return Product.objects.none()

            ids = []
            stack = [category]
            while stack:
                current = stack.pop()
                ids.append(current.id)
                stack.extend(current.subcategories.all())

            urunler = Product.objects.filter(category_id__in=ids)
        elif q:
            urunler = Product.objects.filter(name__icontains=q)
        else:
            return Product.objects.none()
        
        gruplar = {}
        for filtre in ozel:
            if ':' not in filtre:
                continue
            isim, deger = filtre.split(':', 1)
            gruplar.setdefault(isim.strip(), []).append(deger.strip())

        for isim, degerler in gruplar.items():
            urunler = urunler.filter(
                ozellik_degerleri__attribute__isim=isim,
                ozellik_degerleri__value__in=degerler,
            )
        

        genel_kosul = Q()
        for alan in genel:
            if alan in self.GENEL_ALANLAR:
                genel_kosul |= Q(**{alan: True})

        if genel_kosul:
            urunler = urunler.filter(genel_kosul)

        return urunler.distinct()