import datetime
import json

from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.cache import cache

from .game_handlers.game_logic import (
    GameFinished, NotPlayersTurn, PlayerDead, square_clicked
)
from .game_handlers.message_handler import input_handler


# Game Consumer, Game WS Connection Handler
class GameConsumer(AsyncWebsocketConsumer):
    # Connect
    async def connect(self):
        # Add the user to the game group
        self.game_id = self.scope["url_route"]["kwargs"]["game_id"]
        await self.channel_layer.group_add(
            self.game_id,
            self.channel_name,
        )
        # Checking game and the game plysers
        game_state = await cache.aget(f"game:{self.game_id}")

        if game_state is None:
            return

        game_players = game_state["players"]

        if len(game_players.keys()) > 1:
            # Start The game and Send the Game Status
            await self.channel_layer.group_send(self.game_id, {"type": "Send_Game", "data": game_state})
        else:
            # Send The Game Players Status
            await self.channel_layer.group_send(
                self.game_id,
                {"type": "Update_Members", "data": game_players},
            )

        await self.accept()

    # Disconnect
    async def disconnect(self, close_code):
        # Remove the user from the game group
        await self.channel_layer.group_discard(self.game_id, self.channel_name)

    # Receive messages from frontend websocket connection
    async def receive(self, text_data):
        payload_json = json.loads(text_data)

        # Send the message to the group based on the message method
        if payload_json["method"] == "update_game":
            data = payload_json["data"]
            player_name = data["player_name"]
            click_at = data["click_at"]  # should = list or tuple

            game_state = await cache.aget(f"game:{self.game_id}")
            if game_state:
                try:
                    square_clicked(game_state, player_name, *click_at)
                    await cache.aset(f"game:{self.game_id}", game_state)
                    # Hint For Improve :
                    # - Now i am sending the whole game_state at each click after update it
                    # - That will be heavy on the frontend and on the WS connection
                    # - Maybe send just the changes only will be better

                    await self.channel_layer.group_send(self.game_id, {"type": "Update_Game", "data": game_state})
                except (PlayerDead, GameFinished, NotPlayersTurn):
                    pass

    # Handlers
    # Receive message from group

    # Start Game Handler
    async def Send_Game(self, event):
        data = event["data"]
        # Send message to WebSocket connection on the frontend
        await self.send(text_data=json.dumps({"method": "start_game", "data": data}))

    # Update Members Handler
    async def Update_Members(self, event):
        data = event["data"]
        # Send message to WebSocket connection on the frontend
        await self.send(text_data=json.dumps({"method": "update_members", "data": data}))

    # Update Game status Handler
    async def Update_Game(self, event):
        data = event["data"]
        # Send message to WebSocket connection on the frontend
        await self.send(text_data=json.dumps({"method": "update_game", "data": data}))


# Chat Consumer, Chat WS Connection Handler


class ChatConsumer(AsyncWebsocketConsumer):
    # Connect
    async def connect(self):
        self.user = self.scope["url_route"]["kwargs"]["username"]
        self.game_code = self.scope["url_route"]["kwargs"]["game_code"]
        self.room_group_name = f"chat-{self.game_code}"
        # Add the user to the game-chat group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    # Disconnect
    async def disconnect(self, code):
        # Remove the user from the game-chat group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive messages from frontend websocket connection
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json["username"]
        game_code = text_data_json["game_code"]

        data = {
            "message": message,
            "username": username,
            "game_code": game_code,
        }
        # Send the message to the game-chat group based on the Message type
        is_regular_message = await input_handler(data)
        date_now = datetime.datetime.now().strftime("%I:%M %p")

        if is_regular_message[0] is True:
            # Regular Message => Send it as it is
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
            # Command Message => Send a notification
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "send_notification",
                    "message": message,
                    "username": username,
                    "cmd": cmd,
                    "date": date_now,
                },
            )

    # Handlers
    # Receive message from group

    # Regular Message Handler
    async def send_messages(self, event):
        message = event["message"]
        username = event["username"]
        date = event["date"]
        # Send message to WebSocket connection on the frontend
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

    # Notification Handler
    async def send_notification(self, event):
        message = event["message"]
        username = event["username"]
        cmd = event["cmd"]
        date = event["date"]
        await self.send(
            text_data=json.dumps(
                {
                    "method": "NTF",
                    "message": message,
                    "username": username,
                    "cmd": cmd,
                    "date": date,
                }
            )
        )
