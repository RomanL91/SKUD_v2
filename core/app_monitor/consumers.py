import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class WebClientConsumer(WebsocketConsumer):

    def connect(self):
        self.accept()
        async_to_sync(self.channel_layer.group_add)(
            "client",
            self.channel_name,
        )


    def recv(self, event):
        print("Consumer received smthing from channels")
        

    def disconnect(self, close_code):
        self.channel_layer.group_discard("client",self.channel_name)


    def receive(self, text_data):
        self.send(text_data=json.dumps({"event": text_data["text_data"]})) # WORK!! 
