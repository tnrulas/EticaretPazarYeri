from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from .models import Payment
from .serializer import PaymentSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
import uuid
from django.db import transaction
from orders.models import Order, OrderItem
from rest_framework.views import APIView
from django.db.models import F

# Create your views here.

class PaymentCreateView(APIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    @transaction.atomic
    def post(self, request, order_id):
        
        order = get_object_or_404(Order, id=order_id, buyer=request.user)

        if order.is_verified:
            return Response({"error": "Bu siparişin ödemesi zaten yapılmış."}, status=status.HTTP_400_BAD_REQUEST)
        
        order_items = OrderItem.objects.filter(order=order)
        amount = 0
        for item in order_items:
            amount += item.product.price
        
        is_successful = True 
        fake_transaction_id = str(uuid.uuid4())
        
        payment = Payment.objects.create(
            user=request.user,
            order=order,
            amount=amount,
            is_successful=is_successful,
            transaction_id=fake_transaction_id
        )
        
        order.is_verified = True
        order.save()
        
        for item in order_items:
            product = item.product
            
            product.stock_count = F('stock_count') - item.quantity
            
            product.save()
        
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)