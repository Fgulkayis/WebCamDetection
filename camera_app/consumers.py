import json
from channels.generic.websocket import WebsocketConsumer

class CameraConsumer(WebsocketConsumer):
    def connect(self):

        self.accept() 

        print("WebSocket bağlantısı kuruldu!")

        self.send(text_data=json.dumps({
            'message': 'WebSocket bağlantısı başarıyla kuruldu!'
        }))

    def disconnect(self, close_code):

        print("WebSocket bağlantısı kapandı:", close_code)

    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        print(f"İstemciden gelen mesaj: {message}")


        self.send(text_data=json.dumps({
            'message': f'Sunucudan yanıt: {message}'
        }))