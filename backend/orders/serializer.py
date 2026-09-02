from .models import Address, CartItem, Order, OrderItem
from rest_framework import serializers

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'user', 'street', 'city', 'zip_code']
        read_only_fields = ['user']

class ShowCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id' ,'buyer', 'product', 'quantity']
        read_only_fields = ['buyer']

class OrderItemSerializer(serializers.ModelSerializer):
    
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_photo = serializers.ImageField(source='product.photo', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = OrderItem
        # Yeni eklediğimiz alanları fields listesine mutlaka yazıyoruz
        fields = ['id', 'product', 'product_name', 'product_photo', 'product_price', 'quantity', 'address']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id' ,'buyer', 'address', 'created_at', 'is_verified', 'items']
        read_only_fields = ['buyer', 'is_verified', 'items']