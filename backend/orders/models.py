from django.db import models

# Create your models here.

class Address(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='addresses')
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} - {self.city}"

class CartItem(models.Model):
    buyer = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

class Order(models.Model):
    buyer = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()