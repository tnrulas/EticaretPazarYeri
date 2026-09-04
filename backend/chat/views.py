from django.shortcuts import render
from rest_framework import generics, status
from .serializer import MesajlasmaAlaniSerializer, MesajOlusturSerializer, MesajListeleSerializer
from .models import MesajlasmaAlani, Mesaj
from rest_framework.permissions import IsAuthenticated
from accounts.models import CustomUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models import Q


# Create your views here.
class MesajlasmaAlaniOlusturView(generics.CreateAPIView):
    serializer_class = MesajlasmaAlaniSerializer
    permission_classes = [IsAuthenticated]
    
    
    def create(self, request, *args, **kwargs):

        satici_id = request.data.get('satici_id')
        
        if not satici_id:
            return Response({"error": "Satıcı ID'si gönderilmedi."}, status=status.HTTP_400_BAD_REQUEST)
        
        satici = get_object_or_404(CustomUser, id=satici_id)
        
        if request.user == satici:
            return Response({"error": "Kendinizle mesajlaşma alanı oluşturamazsınız."}, status=status.HTTP_400_BAD_REQUEST)
        
        if satici.is_buyer == False:
            return Response({"error": "mesajlaşma alanı oluşabilmesi için alıcı ve satıcı olmalıdır."}, status=status.HTTP_400_BAD_REQUEST)
        
        oda, created = MesajlasmaAlani.objects.get_or_create(
            alici=request.user,
            satici=satici,
            defaults={'isim': f"{request.user.username} ve {satici.username} Sohbeti"}
        )
        
        serializer = self.get_serializer(oda)
        
        
        donus_kodu = status.HTTP_201_CREATED if created else status.HTTP_200_OK
        return Response(serializer.data, status=donus_kodu)

class MesajOlusturView(generics.CreateAPIView):
    serializer_class = MesajOlusturSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        mesajlasma_alani_id = request.data.get('mesajlasma_alani')
        icerik = request.data.get('icerik', '').strip()
        
        if not icerik:
            return Response(
                {'error': 'Boş mesaj gönderemezsiniz.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        oda_gecerli_mi = MesajlasmaAlani.objects.filter(
            id=mesajlasma_alani_id
        ).filter(
            Q(alici=request.user) | Q(satici=request.user)
        ).exists()
        
        if not oda_gecerli_mi:
            return Response(
                {'error': 'Oda bulunamadı veya bu odaya erişim izniniz yok.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        mesaj = Mesaj.objects.create(
            mesajlasma_alani_id=mesajlasma_alani_id,
            gönderici=request.user,
            icerik=icerik,
            gönderilme_tarihi=timezone.now()
        )
        
        serializer = self.get_serializer(mesaj)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MesajListView(generics.ListAPIView):
    serializer_class = MesajListeleSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        mesajlasma_alani_id = self.kwargs.get('mesajlasma_alani_id')
        return Mesaj.objects.filter(mesajlasma_alani_id=mesajlasma_alani_id)
    
    def list(self, request, *args, **kwargs):
        mesajlasma_alani_id = self.kwargs.get('mesajlasma_alani_id')
        
        if not MesajlasmaAlani.objects.filter(
            id=mesajlasma_alani_id,
            alici=request.user
        ).exists() and not MesajlasmaAlani.objects.filter(
            id=mesajlasma_alani_id,
            satici=request.user
        ).exists():
            return Response(
                {'error': 'Bu mesajlaşma alanına erişim izniniz yok.'}, status=status.HTTP_403_FORBIDDEN
            )
        
        return super().list(request, *args, **kwargs)