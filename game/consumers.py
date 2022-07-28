import datetime
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

from .game_handlers.message_handler import input_handler


# GAME HANDLER
class GameConsumer(AsyncWebsocketConsumer):
    # conect
    async def connect(self):
        # connect the user to the game group
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        await self.channel_layer.group_add(
            self.game_id,
            self.channel_name,
        )
        game_state = cache.get(f"game:{self.game_id}")
        game_players = game_state["players"]
        if game_state:
            if len(game_players.keys()) >= 4:

                # GameLogic = cache.get(f"game:logic:{self.game_id}")
                # Game = {"game_members": GameMembers, "game_logic": GameLogic}
                await self.channel_layer.group_send(
                    self.game_id, {"type": "Send_Game", "data": game_state}
                )
            else:
                await self.channel_layer.group_send(
                    self.game_id, {"type": "Send_Memebers", "data": game_players}
                )

        await self.accept()

    ## disconnect
    async def disconnect(self, close_code):
        ## disconnect the user from the game group
        await self.channel_layer.group_discard(self.game_id, self.channel_name)

    ## receive messages from the frontend
    async def receive(self, text_data):
        payload_json = json.loads(text_data)

        ## Send message to each user in the group based on what received
        if payload_json["method"] == "update_game":
            data = payload_json["data"]
            await self.channel_layer.group_send(
                self.game_id, {"type": "update_game", "data": data}
            )

    ## handlers

    ## click method handler
    async def Send_Game(self, event):
        data = event["data"]

        ## Send message to WebSocket
        await self.send(text_data=json.dumps({"method": "start_game", "data": data}))

    ## click method handler
    async def Send_Memebers(self, event):
        data = event["data"]

        ## Send message to WebSocket
        await self.send(
            text_data=json.dumps({"method": "update_members", "data": data})
        )


# MESSAGE HANDLER


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["url_route"]["kwargs"]["username"]
        self.game_code = self.scope["url_route"]["kwargs"]["game_code"]
        self.room_group_name = f"chat-{self.game_code}"
        print(self.room_group_name)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        message = text_data_json["message"]
        username = text_data_json["username"]
        game_code = text_data_json["game_code"]

        data = {"message": message, "username": username, "game_code": game_code}

        is_regular_message = input_handler(data)

        date_now = datetime.datetime.now().strftime("%I:%M %p")
        if is_regular_message[0] is True:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "send_messages",
                    "message": message,
                    "username": username,
                    "date": date_now,
                },
            )
        else:
            cmd = is_regular_message[1]
            message = f"Congrat!! You Hited the {cmd} command"
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "send_notification",
                    "message": message,
                    "username": username,
                    "date": date_now,
                },
            )

    async def send_messages(self, event):
        message = event["message"]
        username = event["username"]
        date = event["date"]
        await self.send(
            text_data=json.dumps(
                {
                    "method": "MSG",
                    "message": message,
                    "username": username,
                    "date": date,
                }
            )
        )

    async def send_notification(self, event):
        message = event["message"]
        date = event["date"]
        # cmd = event['cmd']
        await self.send(
            text_data=json.dumps(
                {
                    "method": "NTF",
                    "message": message,
                    # "cmd":cmd,
                    "date": date,
                }
            )
        )
