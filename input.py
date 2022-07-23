commands = []  # list of command triggers


def message_handler(message):
    pass


def command_handler(message: str, cmd: str):
    pass


def command_validator(message: str) -> list:
    """
    Tests if the command is valid

    If the command is invalid, returns False and "Too many commands passed, maximum of 1 allowed"
    """

    command_count = 0   # Command count
    command = ""        # Null handling

    for i in message.lower().split():
        if i in commands:  # only allows for 1 command per string

            # If count is 1, that means it has more commands in it, so return False
            if command_count >= 1:
                return [False, "Too many commands passed, maximum of 1 allowed"]

            command_count += 1
            command = i

    command_handler(message, command)  # In the end, pass the message and command to the message handler to execute it

    return [True]  # Tell that it was a command


def input_handler(message: str) -> None:  # Pass the chat message to this function
    """
    Main chat handler

    If the function is a command, run it
    If it isn't, pass the message to the message handler
    """
    is_command = False

    for i in message.lower().split():

        if i in commands:
            is_command = True
            validator_response = command_validator(message)  # Validates if the message is a command

            if not validator_response[0]:
                pass  # tell the user what the error is. Error message is ret[1]

    if not is_command:
        message_handler(message)  # Passes the non-command message to the message handler
