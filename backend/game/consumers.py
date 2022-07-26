from channels.generic.websocket import AsyncWebsocketConsumer
import json
from django.core.cache import cache
import datetime



# GAME HANDLER
class GameConsumer(AsyncWebsocketConsumer):
    ## conect
    async def connect(self):
        ## connect the user to the game group
        self.game_id = self.scope['url_route']['kwargs']['game_id']
        await self.channel_layer.group_add(
            self.game_id,
            self.channel_name,

        )
        GameMembers = cache.get(f'game:members:{self.game_id}')
        if len(GameMembers.keys()) >= 4:
            
            GameLogic = cache.get(f'game:logic:{self.game_id}')
            Game = {
                'game_members':GameMembers,
                "game_logic":GameLogic
            }
            await self.channel_layer.group_send(self.game_id, {"type": "Send_Game", "data": Game})
        else:
            await self.channel_layer.group_send(self.game_id, {"type": "Send_Memebers", "data": GameMembers})

        await self.accept()


    ## disconnect
    async def disconnect(self, close_code):
        ## disconnect the user from the game group
        await self.channel_layer.group_discard(
            self.game_id,
            self.channel_name
        )
    ## receive messages from the frontend
    async def receive(self, text_data):
        payload_json = json.loads(text_data)

    

        ## Send message to each user in the group based on what received
        if payload_json['method'] == "update_game":
            data = payload_json['data']
            await self.channel_layer.group_send(
                self.game_id,
                {
                    'type': 'update_game',
                    'data': data
                }
            )

    ## handlers

    ## click method handler
    async def Send_Game(self, event):
        data = event['data']

        ## Send message to WebSocket
        await self.send(text_data=json.dumps({
            'method':'start_game',
            'data': data
        }))
    ## click method handler
    async def Send_Memebers(self, event):
        data = event['data']

        ## Send message to WebSocket
        await self.send(text_data=json.dumps({
            'method':'update_members',
            'data': data
        }))
    

# MESSAGE HANDLER

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['url_route']['kwargs']['username']
        self.game_code = self.scope['url_route']['kwargs']['game_code']
        self.room_group_name = f"chat:{self.game_code}"
        print(self.room_group_name)
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # await self.channel_layer.group_send( 
        #     self.room_group_name,
        #     {
        #         'type':'send_notification',
        #         'msg_type':'notify',
        #         'username':self.user.username,
        #         'message': f'{self.user.username} joined the chat',
        #         'date': datetime.datetime.now().strftime("%I:%M %p | %d %b %Y")
        #     }
        # )
        await self.accept()


    

    
    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
 

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        date_now = datetime.datetime.now().strftime("%I:%M %p | %d %b %Y")
        await self.save_message(text_data_json)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_messages',
                'msg_type':'con',
                'message': message,
                'username': username,
                'date': date_now,
            }
        )
    async def send_messages(self,event):
        message = event['message']
        msg_type = event['msg_type']
        username = event['username']
        date = event['date']
        await self.send(text_data=json.dumps({
            'msg_type':msg_type,
            'message': message,
            'username': username,
            'date': date,
        }))

    # async def send_notification(self,event):
    #     message = event['message']
    #     msg_type = event['msg_type']
    #     username = event['username']
    #     date = event['date']
    #     await self.send(text_data=json.dumps({
    #         'msg_type': msg_type,
    #         'username': username,
    #         'message': message,
    #         'date': date,
    #     }))
