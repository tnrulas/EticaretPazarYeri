from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status

from accounts.models import CustomUser
from .models import Product, Review, ImageProduct, Category, CategoryAttribute, ProductValue, VisitedProduct
from .serializer import ProductSerializer, ProductReviewSerializer, CategorySerializer, ProductValueSerializer, VisitedProductSerializer, ProductVariantSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from orders.models import OrderItem
import json
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from rest_framework.views import APIView

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

        varyant_serializer = None
        varyant_str = self.request.data.get('varyant')
        if varyant_str:
            try:
                varyant_data = json.loads(varyant_str)
            except json.JSONDecodeError:
                raise ValidationError("varyant JSON formatında olmalıdır.")

            varyant_serializer = ProductVariantSerializer(data=varyant_data)
            varyant_serializer.is_valid(raise_exception=True)

            toplam = sum(s['stok'] for s in varyant_serializer.validated_data['secenekler'])
            urun_stok = serializer.validated_data['stock_count']
            if toplam != urun_stok:
                raise ValidationError(f"Varyant stokları toplamı ({toplam}) ürün stoğuna ({urun_stok}) eşit olmalı.")
        
        product = serializer.save(seller=self.request.user)

        if varyant_serializer:
            varyant = varyant_serializer.save()
            product.variantes = varyant
            product.save()
        
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

class ProductAllReviewView(generics.ListAPIView):
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.filter(user=self.request.user).order_by('-created_at')

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

class VisitedProductAddView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get('product_id')
        user_id = request.data.get('user_id')

        if str(request.user.id) != str(user_id):
            raise PermissionDenied("Başka bir kullanıcı adına ziyaret kaydı eklenemez.")

        user = get_object_or_404(CustomUser, id=user_id)
        product = get_object_or_404(Product, id=product_id)

        _, olusturuldu = VisitedProduct.objects.get_or_create(name=user, product=product)
        if not olusturuldu:
            return Response({"mesaj": "Bu ürün zaten ziyaret edilenlerde"}, status=status.HTTP_200_OK)

        if VisitedProduct.objects.filter(name=user).count() > 20:
            en_eski = VisitedProduct.objects.filter(name=user).order_by('id').first()
            en_eski.delete()

        return Response({"mesaj": "Ziyaret kaydedildi"}, status=status.HTTP_201_CREATED)

class VisitedProductListView(generics.ListAPIView):
    serializer_class = VisitedProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return VisitedProduct.objects.filter(name=self.request.user).order_by('-id')