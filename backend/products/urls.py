from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('Urunliste/', ProductListView.as_view(), name='urun-liste'),
    path('Urunliste/<int:pk>/', ProductDetailView.as_view(), name='urun-detay'),
    path('Urunekle/', ProductCreateView.as_view(), name='urun-ekle'),
    path('ara/', ProductSearchFilterView.as_view(), name='urun-ara'),
    path('Urunliste/<int:product_id>/yorumlar/', ProductReviewView.as_view(), name='urun-yorumlari'),
    path('kategori/', ProductCategoryListView.as_view(), name='urun-kategori'),
    path('satici/<int:seller_id>/', SellerProductListView.as_view())
]