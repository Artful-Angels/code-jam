from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
from django.core.cache import cache

from .game_logic import (
    CommandFailed, GameFinished, NotPlayersTurn, PlayerDead,
    close_open_squares, delete_square, new_life, roll_winner
)

channel_layer = get_channel_layer()

commands = ["delete", "winner", "new", "close"]  # list of commands


@sync_to_async
def command_handler(data: dict) -> bool:
    """
    Handles the commands

    For each command there will be a handler
    """
    nickname = data["username"]
    cmd = data["cmd"]
    game_code = data["game_code"]
    game_state = cache.get(f"game:{game_code}")

    if game_state["is_finished"]:
        return False

    elif cmd == "delete":
        if not game_state["players"][nickname]["is_alive"]:
            return False
        try:
            new_game_state = delete_square(game_state, nickname)
            cache.set(f"game:{game_code}", new_game_state)
            async_to_sync(channel_layer.group_send)(str(game_code), {"type": "Update_Game", "data": new_game_state})
        except (CommandFailed, PlayerDead, GameFinished, NotPlayersTurn):
            return False
    elif cmd == "winner":
        try:
            new_game_state = roll_winner(game_state, nickname)
            cache.set(f"game:{game_code}", new_game_state)
            async_to_sync(channel_layer.group_send)(str(game_code), {"type": "Update_Game", "data": new_game_state})
        except CommandFailed:
            return False
    elif cmd == "new":
        try:
            new_game_state = new_life(game_state, nickname)
            cache.set(f"game:{game_code}", new_game_state)
            async_to_sync(channel_layer.group_send)(str(game_code), {"type": "Update_Game", "data": new_game_state})
        except CommandFailed:
            return False
    elif cmd == "close":
        try:
            new_game_state = close_open_squares(game_state, nickname)
            cache.set(f"game:{game_code}", new_game_state)
            async_to_sync(channel_layer.group_send)(str(game_code), {"type": "Update_Game", "data": new_game_state})
        except CommandFailed:
            return False
    return True


def command_validator(message: str) -> list:
    """
    Tests if the command is valid

    If the command is invalid, returns False and "Too many commands passed, maximum of 1 allowed"
    """
    message = message.lower().split()  # Splits the message into a lowercase list for further processing
    command_count = 0  # Command count
    command_index = None

    for index, value in enumerate(message):
        if value in commands:  # only allows for 1 command per string

            # If count is 1, that means it has more commands in it, so return False
            if command_count >= 1:
                return [False]

            command_count += 1
            command_index = index

    # In the end, pass the message and command to the message handler to execute it
    cmd = message[command_index]
    return [True, cmd]  # Tell the runner that the message was a command


async def input_handler(data: dict) -> list[bool]:
    """
    Main chat handler

    If the function is a command, run it
    If it isn't, pass the message to the message handler
    """
    message = data["message"]
    is_command = False

    for i in message.lower().split():
        if i in commands:
            validator_response = command_validator(message)  # Validates if the message is a command

            if not validator_response[0]:
                return [True]

            data["cmd"] = validator_response[1]
            command_result = await command_handler(data)
            if command_result:
                return [False, validator_response[1]]
            else:
                return [True]

    if not is_command:
        return [True]
