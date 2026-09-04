from django.db import models

# Create your models here.
class MesajlasmaAlani(models.Model):
    isim = models.CharField(max_length=100, null=True, blank=True)
    alici = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='alici_side')
    satici = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='satici_side')
    olusturulma_tarihi = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        katilimcilar = [str(self.alici), str(self.satici)]
        return f"mesajlasma alanı {self.id} - katılımcılar: {katilimcilar}"

class Mesaj(models.Model):
    mesajlasma_alani = models.ForeignKey(MesajlasmaAlani, on_delete=models.CASCADE, related_name='mesajlar')
    gönderici = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='gönderici_mesajlar')
    icerik = models.TextField()
    gönderilme_tarihi = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"mesajı gönderen kişi: {self.gönderici.username} - mesaj içeriği: {self.icerik[:20]}"