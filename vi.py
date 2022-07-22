commands = [] #list of command triggers


def message_handler(message):
    pass


def command_handler(message: str, cmd: str):
    pass


def command_validator(message: str):
    msg = message.lower().split()
    count = 0

    for i in msg:
        if i in commands: #only allows for 1 command per string
            if count == 0:
                count += 1 
                cmd = i
            elif count == 1:
                return (False, "Too many commands passed, maximum of 1 allowed")
    command_handler(message, cmd)
    

def input_handler(message: str) -> None:#Pass the chat message to this func
    msg = message.lower().split()
    is_com = False
    for i in msg:
        if i in commands:
            is_com =  True
            ret = command_validator(message)
            if ret[0] == False:
                pass #tell the user what the error is. Error message is ret[1]
    if is_com:
        message_handler(message)
