from rest_framework import serializers
from .models import CustomUser

class CreateCustomSellerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email','company_name', 'company_address', 'company_phone', 'password']
        extra_kwargs = {'password':{'write_only': True}}
    
    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value
    
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    
    def create(self, validated_data):
        validated_data['is_seller'] = True
        user = CustomUser.objects.create_user(**validated_data)
        return user

class CreateCustomBuyerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def validate_username(self, value):
        if CustomUser.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value
    
    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    
    def create(self, validated_data):
        validated_data['is_buyer'] = True
        user = CustomUser.objects.create_user(**validated_data)
        return user