import json
import os

from .history import readHistory

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model

class Chat(AsyncWebsocketConsumer):
    nomorMessage = 0
    
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['user']
        self.room_group_name = 'chat_' + str(self.room_name)

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        # text_data = {
        #     'type': 'chat_message',
        #     'type_message': 'user_disconnect',
        #     'from': self.scope['user'].username
        # }
        # channel_layer = get_channel_layer()
        
        # await channel_layer.group_send(
        #     'chat_{}'.format(self.scope['user'].username),
        #     text_data,
        # )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        dictData = {
            'type': 'chat_message',
            'type_message': text_data_json['type_message'],
            'from': self.scope['user'].username
        }
        if text_data_json['value'] != '' and text_data_json['value'] != None:
            dictData['value'] = text_data_json['value']
        if text_data_json['type_message'] == 'chat_friend':
            dictData['user'] = text_data_json['user']
            self.nomorMessage += 1
            dictData['deterrent'] = self.nomorMessage
            
        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name, dictData)

    # Receive message from room group
    async def chat_message(self, event):

        # Send message to WebSocket / send to server side (front end)
        dictData = {
            'type_message': event['type_message'],
            'value': event['value'] if event['value'] != '' or event['value'] != None else '',
            'from': event['from']
        }
        
        url = 'media/user/history'
        
        if event['type_message'] == 'history_chat':
            dataHistory = readHistory(event['value'])
            
            if dataHistory != "ignore username" and dataHistory != "file not found":
                dictData['value'] = dataHistory
            elif dataHistory == 'file not found':
                user = event['value'].split(' - ')
                dataWrite = {
                    "user": ["{}".format(user[0]), "{}".format(user[1])],
                    "chat": []
                }
                
                with open('{}/{}.json'.format(url, event['value']), 'w') as file:
                    json.dump(dataWrite, file)
                dictData['value'] = 'None'
            elif dataHistory == 'ignore username':
                dictData['value'] = 'None'
            
        if event['type_message'] == 'chat_friend':
            if self.nomorMessage == event['deterrent']:
                self.nomorMessage += 1
                data = readHistory(event['user'])
                data['chat'].append({
                    'from': event['from'],
                    'value': event['value']
                })
                
                if os.path.exists('{}/{}.json'.format(url, event['user'])):
                    with open('{}/{}.json'.format(url, event['user']), 'w') as file:
                        json.dump(data, file)
                elif os.path.exists('{}/{}.json'.format(url, '{} - {}'.format(event['user'].split(' - ')[1], event['user'].split(' - ')[0]))):
                    with open('{}/{}.json'.format(url, '{} - {}'.format(event['user'].split(' - ')[1], event['user'].split(' - ')[0])), 'w') as file:
                        json.dump(data, file)
                    
                dictData['value'] = event['value']
        
        await self.send(text_data=json.dumps(dictData))


class Online(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'user_online'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        text_data = {
                'type': 'chat_message',
                'type_message': 'user_disconnect',
                'from': self.scope['user'].username
        }
        channel_layer = get_channel_layer()
        
        await channel_layer.group_send(
            'user_online',
            text_data,
        )
            
        # async_to_sync(channel_layer.group_send)('user_online', text_data)
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket / user
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        dictData = {
            'type': 'chat_message',
            'type_message': text_data_json['type_message'],
            'from': self.scope['user'].username
        }
        
        # Send message to room group
        await self.channel_layer.group_send(self.room_group_name, dictData)

    # Receive message from room group
    async def chat_message(self, event):

        # Send message to WebSocket / send to server side (front end)
        dictData = {
            'type_message'  : event['type_message'],
            'value' : ''
        }
        if event['type_message'] == 'user_join':
            if event['from'] == self.scope['user'].username:
                dictData = {}
            else:
                dictData['value'] = event['from']
        if event['type_message'] == 'get_user_online':
            if event['from'] == self.scope['user'].username:
                dictData = {}
            else:
                dictData['value'] = event['from']
        if event['type_message'] == 'user_disconnect':
            dictData['value'] = event['from']
        await self.send(text_data=json.dumps(dictData))