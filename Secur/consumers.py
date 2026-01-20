"""
this module contains consumer classes for handling WebSocket connections
"""

import json

from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("Websocket connected")
    async def disconnect(self, close_code):
        print("Websocket disconnected")
    async def receive(self, text_data):
        print(f"recieved: {text_data}")

        
