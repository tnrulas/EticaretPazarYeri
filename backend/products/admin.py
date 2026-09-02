from django.contrib import admin
from .models import *

# Register your models here.

class ImageProductInline(admin.TabularInline):
    model = ImageProduct
    extra = 3

class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageProductInline]
    
    
admin.site.register(Product, ProductAdmin)