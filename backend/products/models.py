from django.db import models
from django.conf import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)
    
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.name} -> {self.name}"
        return self.name

class CategoryAttribute(models.Model):
    FILTRE_TIPLERI = (
        ('secim', 'Çoktan Seçmeli (Dropdown/Checkbox)'),
        ('boolean', 'Aç/Kapa (Toggle)'),
    )
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='ozellikler')
    isim = models.CharField(max_length=100)
    filtre_tipi = models.CharField(max_length=20, choices=FILTRE_TIPLERI, default='secim')
    
    secenekler = models.TextField(blank=True, null=True, help_text="Seçenekleri virgülle ayırarak yazın. (Örn: Kırmızı, Mavi, Siyah)")
    
    def __str__(self):
        return f"{self.category.name} - {self.isim} ({self.get_filtre_tipi_display()})"

class ProductValue(models.Model):
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, related_name='ozellik_degerleri')
    attribute = models.ForeignKey(CategoryAttribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    
    class Meta:
        unique_together = ('product', 'attribute')
    
    def __str__(self):
        return f"{self.product.name} -> {self.attribute.isim}: {self.value}"

class Product(models.Model):
    seller = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='products')
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    photo = models.ImageField(upload_to='product_photos/')
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock_count = models.IntegerField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_bulk_sale = models.BooleanField(default=False)
    is_gift_wrap = models.BooleanField(default=False)
    has_video = models.BooleanField(default=False)
    is_campaign = models.BooleanField(default=False)
    is_buy_together = models.BooleanField(default=False)
    is_buy_more_pay_less = models.BooleanField(default=False)
    is_corporate_invoice = models.BooleanField(default=False)
    is_editor_choice = models.BooleanField(default=False)
    
    # category = models.CharField(blank=True, null=True, max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    brand = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.seller.username}"

class ImageProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_photos/')
    
    def __str__(self):
        return f"{self.product.name} - Galeri Görseli"

class Review(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='reviewer')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='urun')
    is_buyed = models.BooleanField(default=False)
    message = models.TextField(blank=True, null=True)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)