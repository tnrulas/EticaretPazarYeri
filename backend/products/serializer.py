from rest_framework import serializers
from .models import *


class ExtraImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProduct
        fields = ['id', 'image']

class CategoryAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryAttribute
        fields = ['id', 'isim', 'filtre_tipi', 'secenekler']

class CategorySerializer(serializers.ModelSerializer):
    ozellikler = CategoryAttributeSerializer(many=True, read_only=True)
    
    subcategories = serializers.SerializerMethodField()
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent', 'ozellikler', 'subcategories']
    
    def get_subcategories(self, obj):
        if obj.subcategories.exists():
            return CategorySerializer(obj.subcategories.all(), many=True).data
        return []

class ProductValueSerializer(serializers.ModelSerializer):
    attribute_name = serializers.CharField(source='attribute.isim', read_only=True)
    attribute_type = serializers.CharField(source='attribute.filtre_tipi', read_only=True)
    
    class Meta:
        model = ProductValue
        fields = ['id', 'product', 'attribute_name', 'attribute_type', 'value']
        
        read_only_fields = ['product']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'baslik', 'secenekler']

    def validate_secenekler(self, value):
        if not isinstance(value, list) or len(value) == 0:
            raise serializers.ValidationError("En az bir seçenek girilmeli.")

        temiz = []
        gorulen = set()
        for secenek in value:
            if not isinstance(secenek, dict):
                raise serializers.ValidationError("Seçenek formatı hatalı.")

            deger = str(secenek.get('deger', '')).strip()
            if not deger:
                raise serializers.ValidationError("Seçenek adı boş olamaz.")
            if deger.lower() in gorulen:
                raise serializers.ValidationError(f"'{deger}' birden fazla girilmiş.")
            gorulen.add(deger.lower())

            try:
                stok = int(secenek.get('stok'))
            except (TypeError, ValueError):
                raise serializers.ValidationError(f"'{deger}' için stok sayı olmalı.")
            if stok < 0:
                raise serializers.ValidationError(f"'{deger}' için stok negatif olamaz.")

            temiz.append({'deger': deger, 'stok': stok})

        return temiz
        
class ProductSerializer(serializers.ModelSerializer):
    images = ExtraImagesSerializer(many=True, read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    attribute_values = ProductValueSerializer(source='ozellik_degerleri', many=True, read_only=True)
    variantes = ProductVariantSerializer(read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'seller', 'seller_name', 'name', 'description', 'photo', 'price', 'old_price', 'stock_count',
            
            'category', 'category_name', 'brand',
            
            'is_bulk_sale', 'is_gift_wrap', 'has_video', 'is_campaign', 
            'is_buy_together', 'is_buy_more_pay_less', 'is_corporate_invoice', 'is_editor_choice',
            
            'created_at', 'updated_at', 'images', 'attribute_values',
            
            'variantes'
        ]

        read_only_fields = ['seller']

class ProductReviewSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(source='user.username', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_photo = serializers.ImageField(source='product.photo', read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'user', 'username', 'product', 'is_buyed', 'message', 'rating', 'created_at', 'product_name', 'product_photo']
        
        read_only_fields = ['user', 'is_buyed', 'product']

class VisitedProductSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_photo = serializers.ImageField(source='product.photo', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = VisitedProduct
        fields = ['id', 'name', 'product', 'product_name', 'product_photo', 'product_price']

