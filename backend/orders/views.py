from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from .models import Address, CartItem, Order, OrderItem
from .serializer import *
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db import transaction

# Create your views here.

class AddressCreateView(generics.CreateAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AddressListView(generics.ListAPIView):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

class CartItemCreateView(generics.CreateAPIView):
    serializer_class = ShowCartItemSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)

class CartItemListView(generics.ListAPIView):
    serializer_class = ShowCartItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CartItem.objects.filter(buyer=self.request.user)

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request):
        address_id = request.data.get('address')
        if not address_id:
            return Response({"error": "A dres id si gereklidir."}, status=status.HTTP_400_BAD_REQUEST)
        
        address = get_object_or_404(Address, id=address_id, user=request.user)
        
        cart_items = request.data.get('items', [])
        if not cart_items or len(cart_items) == 0:
            return Response({"error": "Sepetiniz boş."}, status=status.HTTP_400_BAD_REQUEST)
        
        order = Order.objects.create(buyer=request.user, address=address)
        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product_id=item.get('product'),
                quantity=item.get('quantity', 1),
                address=address
            )
        
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)