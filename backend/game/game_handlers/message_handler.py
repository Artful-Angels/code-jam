from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer
from django.core.cache import cache

from .game_logic import delete_square, roll_winner

channel_layer = get_channel_layer()

commands = ["delete", "winner"]  # list of commands


@sync_to_async
def command_handler(data: dict) -> None:
    """
    Handles the commands

    For each command there will be a handler
    """
    print("command_handler Called 3")
    cmd = data["cmd"]
    nickname = data["username"]
    game_code = data["game_code"]
    # print(data)
    # print(type(game_code))
    game_state = cache.get(f"game:{game_code}")
    if cmd == "delete":
        print("if statment done 4")
        # here the (delete) command logic will be
        # in any error case return False
        # try:
        new_game_state = delete_square(game_state, nickname)
        cache.set(f"game:{game_code}", new_game_state)
        print("cache set with changes 7")
        async_to_sync(channel_layer.group_send)(str(game_code), {"type": "Update_Game", "data": new_game_state})
        # except:
        #     return False

        # print("changing the game status based on the delete command")
    elif cmd == "winner":
        # here the (winner) command logic will be
        # in any error case return False
        # try:
        game_state = roll_winner(game_state, nickname)
        cache.set(f"game:{game_code}", new_game_state)
        async_to_sync(channel_layer.group_send)(game_code, {"type": "Update_Game", "data": new_game_state})
        # except:
        #     return False
        # print("changing the game status based on the winner command")

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


async def input_handler(data: dict) -> None:
    """
    Main chat handler

    If the function is a command, run it
    If it isn't, pass the message to the message handler
    """
    print("input_handler Called 2")
    message = data["message"]
    is_command = False

    for i in message.lower().split():
        if i in commands:
            is_command = True
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
