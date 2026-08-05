from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'seller', 'name', 'description', 'photo', 'price', 'stock_count', 'created_at', 'updated_at']

        read_only_fields = ['seller']