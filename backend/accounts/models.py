from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class CustomUser(AbstractUser):
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    
    
    company_name = models.CharField(max_length=255, blank=True, null=True)
    company_address = models.TextField(blank=True, null=True)
    company_phone = models.CharField(max_length=11, blank=True, null=True)
    
    
    
    email = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.username} - {'Satıcı' if self.is_seller else 'Alıcı'}"