from random import randint
from itertools import product


class NicknameTaken(ValueError):
    pass 


class PlayerDead(Exception):
    pass


def number_of_mines(width: int, height: int) -> int:

    lower = (width * height) // 5
    upper = (width * height) // 4
    return randint(lower, upper)


def _generate_mines(mines: int, width: int, height: int) -> dict:

    _mine_state = {(x, y): {
            "coordinates": (x, y),
            "is_open": False,
            "is_mine": False,
            "adjacent_mines": 0
        }
        for y in range(height) for x in range(width)
    }

    for mine in range(mines):
        x, y = randint(0, width-1), randint(0, height-1)
        while _mine_state[(x, y)]["is_mine"]:
            x, y = randint(0, width-1), randint(0, height-1)
        _mine_state[(x, y)]["is_mine"] = True

    return _mine_state


def get_coords(game_state: dict, x: int, y: int):

    coords = set(product([x-1, x, x+1], [y-1, y, y+1])) - {(x, y)}
    return {(x, y) for (x, y) in coords if 0 <= x < game_state["width"] and 0 <= y < game_state["height"]}

 
def _adjacent_mines(game_state: dict, x: int, y: int) -> None:

    coords = get_coords(game_state, x, y)

    return sum(game_state["squares"].get(coord).get("is_mine") for coord in coords)
    

def _decrease_values(game_state: dict, x: int, y: int) -> int:

    mines = 0
    coords = get_coords(game_state, x, y)

    for x, y in coords:
        square = game_state["squares"][(x, y)]
        if square["is_mine"]:
            mines += 1
        elif square["adjacent_mines"] > 0:
            square["adjacent_mines"] -= 1

    return mines


def _reveal_zeros(game_state: dict, x: int, y: int, reveal: bool=True) -> None:

    coords = get_coords(game_state, x, y)
    print("coords", coords, x, y)
    
    for x, y in coords:
        square = game_state["squares"][(x, y)]
        if square["is_open"] == False and square["adjacent_mines"] == 0:
            _reveal_zeros(game_state, x, y)
        if reveal:
            square["is_open"] = True


def _scan_for_zeros(game_state: dict, x: int, y: int) -> None:

    coords = get_coords(game_state, x, y).union({(x, y)})
    for x, y in coords:
        square = game_state["squares"][(x, y)]
        square["is_open"] = True
        if square["adjacent_mines"] == 0:
            _reveal_zeros(game_state, x, y)


def _diffuse_start_squares(game_state: dict, x: int, y: int):

    coords = get_coords(game_state, x, y).union({(x, y)})

    for x, y in coords:
        square = game_state["squares"][(x, y)]
        if square["is_mine"]:
            square["is_mine"] = False
            square["adjacent_mines"] = 0
            _decrease_values(game_state, x, y)
            square["adjacent_mines"] = _adjacent_mines(game_state, x, y)

    game_state["squares"][(x, y)]["adjacent_mines"] = 0


def square_clicked(game_state: dict, nickname: str, x: int, y: int) -> dict:

    square = game_state["squares"][(x, y)]
    player = game_state["players"][nickname]

    if not game_state["players"][nickname]["is_alive"]:
        raise PlayerDead()
    elif not game_state["is_started"]:
        _diffuse_start_squares(game_state, x, y)
        _scan_for_zeros(game_state, x, y)
    elif square["is_mine"]:
        player["is_alive"] = False
        game_state["is_finished"] = True
        for player in game_state["players"]:
            if game_state["players"][player]["is_alive"]:
                game_state["is_finished"] = False
                break
    elif _is_won(game_state):
        game_state["is_finished"] = True
    else:
        square["is_open"] = True
        _reveal_zeros(x, y, reveal=False)

    return game_state


def _is_won(game_state: dict) -> True:

    squares = game_state["squares"]

    for x, y in squares:
        if not squares[(x, y)]["is_open"]:
            if not squares[(x, y)]["is_mine"]:
                return False

    return True


# this is only for testing
def _reveal_board(game_state: dict):
    print("\t", end="")
    for num in range(game_state["width"]):
        print(num % 10, end=" ")
    print("\n")
    for row in range(game_state["height"]):
        print(row % 10, end="\t")
        for col in range(game_state["width"]):
            square = game_state["squares"][(col, row)]
            if square["is_open"]:
                if square["is_mine"]:
                    print("M", end=" ")
                else:
                    print(square["adjacent_mines"], end=" ")
            else:
                print("?", end=" ")
        print()


def create_game(game_code: int, mines: int = 100, width: int = 30, height: int = 16):

    _mine_state = _generate_mines(mines, width, height)

    game_state = {
        "game_code": game_code,
        "is_started": False,
        "is_finished": True,
        "width": width,
        "height": height,
        "players": {},
        "squares": _mine_state,
    }

    for (x, y) in _mine_state:
        value = _adjacent_mines(game_state, x, y)
        game_state["squares"][(x, y)]["adjacent_mines"] = value

    return game_state


def add_member_to_game(game_state: dict, nickname: str) -> None:

    if nickname in game_state["players"]:
        raise NicknameTaken() 
    else:    
        game_state["players"][nickname] = {"nickname": nickname, "is_alive": True}


def eliminate_player(game_state: dict, nickname: str) -> None:

    game_state["players"][nickname]["is_alive"] = False


game_state = create_game(11111)
add_member_to_game(game_state, "Will")
add_member_to_game(game_state, "Vestergurkan")
add_member_to_game(game_state, "Annunaki")
_reveal_board(game_state)
square_clicked(game_state, "Will", 0, 0)
_reveal_board(game_state)
