from django.db import models

# Create your models here.
class Payment(models.Model):
    user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='payments')
    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_successful = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Sipariş No: {self.order.id} - Başarılı: {self.is_successful}"