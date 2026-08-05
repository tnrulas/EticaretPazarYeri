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
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    class Meta:
        model = Order
        fields = ['id' ,'buyer', 'address', 'created_at', 'is_verified', 'items']
        read_only_fields = ['buyer', 'is_verified', 'items']