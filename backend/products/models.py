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
    
    def __str__(self):
        return f"{self.name} - {self.seller.username}"