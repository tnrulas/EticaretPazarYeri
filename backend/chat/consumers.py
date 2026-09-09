from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import MesajlasmaAlani, Mesaj
import json
from django.db import close_old_connections
from django.db.models import Q

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.alan_id = self.scope['url_route']['kwargs']['alan_id']
        self.room_group_name = f'chat_{self.alan_id}'
        self.user = self.scope['user']
        
        if not self.user.is_authenticated:
            await self.close()
            return
        
        katılımcı_mı = await self.katilimci_kontrol()
        if not katılımcı_mı:
            await self.close()
            return
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
    
    async def disconnect(self, close_code):
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        mesaj = data.get('mesaj', '').strip()
        
        if not mesaj or not self.user.is_authenticated:
            return
        
        mesaj_obj = await self.mesaj_kaydet(mesaj)
        
        try:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'id': self.user.id,
                    'username': self.user.username,
                    'mesaj': mesaj_obj.icerik,
                    'gönderilme_tarihi': mesaj_obj.gönderilme_tarihi.isoformat(),
                }
            )
        except Exception as e:
            print(f"\n!!! REDIS YAYIN HATASI !!!: {e}\n")
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'id': event['id'],
            'username': event['username'],
            'mesaj': event['mesaj'],
            'gönderilme_tarihi': event['gönderilme_tarihi'],
        }))
    
    @database_sync_to_async
    def katilimci_kontrol(self):
        close_old_connections()
        try:
            return MesajlasmaAlani.objects.filter(
                id=self.alan_id
            ).filter(
                Q(alici=self.user) | Q(satici=self.user)
            ).exists()
        finally:
            close_old_connections()
    
    @database_sync_to_async
    def mesaj_kaydet(self, mesaj):
        close_old_connections()
        try:
            return Mesaj.objects.create(
                mesajlasma_alani_id=self.alan_id,
                gönderici=self.user,
                icerik=mesaj
            )
        finally:
            close_old_connections()