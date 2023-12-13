import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class UpdateConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def send_update(self, event):
        message = event['message']

        # send the upadate to the websocket
        await self.send(text_data=json.dumps({
            'message': message
        }))