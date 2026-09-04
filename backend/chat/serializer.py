from .models import *
from rest_framework import serializers

class MesajlasmaAlaniSerializer(serializers.ModelSerializer):
    class Meta:
        model = MesajlasmaAlani
        fields = ['id', 'alici', 'satici', 'olusturulma_tarihi']
        
        read_only_fields = ['alici', 'satici', 'olusturulma_tarihi']

class MesajListeleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesaj
        fields = ['id', 'mesajlasma_alani', 'gönderici', 'icerik', 'gönderilme_tarihi']
        
        read_only_fields = ['id', 'mesajlasma_alani', 'gönderici', 'icerik', 'gönderilme_tarihi']

class MesajOlusturSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesaj
        fields = ['mesajlasma_alanı', 'icerik']
        
        read_only_fields = ['mesajlasma_alanı']