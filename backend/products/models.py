from django.db import models
from django.conf import settings

# Create your models here.

class Product(models.Model):
    seller = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to='product_photos/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(blank=True, null=True, max_length=255)
    
    def __str__(self):
        return f"{self.name} - {self.seller.username}"

class Review(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='reviewer')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='urun')
    is_buyed = models.BooleanField(default=False)
    message = models.TextField(blank=True, null=True)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)