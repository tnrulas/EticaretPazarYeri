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
        
class ProductSerializer(serializers.ModelSerializer):
    images = ExtraImagesSerializer(many=True, read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    attribute_values = ProductValueSerializer(source='ozellik_degerleri', many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = [
            'id', 'seller', 'seller_name', 'name', 'description', 'photo', 'price', 'old_price', 'stock_count',
            
            'category', 'category_name', 'brand',
            
            'is_bulk_sale', 'is_gift_wrap', 'has_video', 'is_campaign', 
            'is_buy_together', 'is_buy_more_pay_less', 'is_corporate_invoice', 'is_editor_choice',
            
            'created_at', 'updated_at', 'images', 'attribute_values'
        ]

        read_only_fields = ['seller']

class ProductReviewSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'user', 'username', 'product', 'is_buyed', 'message', 'rating', 'created_at',]
        
        read_only_fields = ['user', 'is_buyed', 'product']