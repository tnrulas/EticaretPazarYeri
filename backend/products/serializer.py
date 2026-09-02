from rest_framework import serializers
from .models import *


class ExtraImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProduct
        fields = ['id', 'image']
class ProductSerializer(serializers.ModelSerializer):
    
    images = ExtraImagesSerializer(many=True, read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'seller', 'name', 'description', 'photo', 'price', 'stock_count', 'created_at', 'updated_at', 'category', 'images', 'seller_name']

        read_only_fields = ['seller']

class ProductReviewSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Review
        fields = ['id', 'user', 'username', 'product', 'is_buyed', 'message', 'rating', 'created_at',]
        
        read_only_fields = ['user', 'is_buyed', 'product']