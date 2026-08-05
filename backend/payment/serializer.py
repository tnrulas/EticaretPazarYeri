from .models import *
from rest_framework import serializers

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'order', 'amount', 'is_successful', 'transaction_id', 'created_at']
        read_only_fields = ['user', 'order', 'transaction_id', 'amount', 'is_successful']