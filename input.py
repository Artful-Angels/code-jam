commands = ["delete"]  # list of commands


def message_handler(message: str) -> None:
    """
    Received message handler

    Sends the message to everyone
    """
    pass


def command_handler(message: list, index: int) -> None:
    """
    Handles the commands

    For each command there will be a handler
    """
    cmd = message[index]

    match cmd:
        # Provide args to the command function through list slicing
        # However many args are expected after the command index
        case "delete":
            print("Delete command activated")
        case _:  # If the command isn't in the list, skip
            print("Unhandled command: " + cmd)     # Debug logs
            print("Original message: " + ' '.join(message))  # Delete at submission!!
            pass


def command_validator(message: str) -> list:
    """
    Tests if the command is valid

    If the command is invalid, returns False and "Too many commands passed, maximum of 1 allowed"
    """
    message = message.lower().split()  # Splits the message into a lowercase list for further processing
    command_count = 0   # Command count
    command_index = None

    for index, value in enumerate(message):
        if value in commands:  # only allows for 1 command per string

            # If count is 1, that means it has more commands in it, so return False
            if command_count >= 1:
                return [False, "Too many commands passed, maximum of 1 allowed"]

            command_count += 1
            command_index = index

    # In the end, pass the message and command to the message handler to execute it
    command_handler(message, command_index)

    return [True]  # Tell the runner that the message was a command


def input_handler(message: str) -> None:
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
                pass  # tell the user what the error is. Error message is validator_response[1]

    if not is_command:
        message_handler(message)  # Passes the non-command message to the message handler
