from itertools import product
from json import dumps
from random import randint


class PlayerDead(Exception):
    """Handles what to do if a dead player clicks a square"""

    pass


class NicknameTaken(ValueError):
    """Handles what to do if a nickname is taken"""

    pass


def number_of_mines(width: int, height: int) -> int:
    """Calculates the number of mines there should be by the height and width"""
    lower = (width * height) // 5
    upper = (width * height) // 4
    return randint(lower, upper)


def _generate_mines(mines: int, width: int, height: int) -> dict:
    _mine_state = {
        dumps([x, y]): {
            "coordinates": (x, y),
            "is_open": False,
            "is_mine": False,
            "adjacent_mines": 0
        }
        for y in range(height) for x in range(width)
    }

    for mine in range(mines):
        x, y = randint(0, width - 1), randint(0, height - 1)
        while _mine_state[dumps([x, y])]["is_mine"]:
            x, y = randint(0, width - 1), randint(0, height - 1)
        _mine_state[dumps([x, y])]["is_mine"] = True

    return _mine_state


def _get_coords(game_state: dict, x: int, y: int):
    coords = set(product([x - 1, x, x + 1], [y - 1, y, y + 1])) - {(x, y)}
    return {(x, y) for (x, y) in coords if 0 <= x < game_state["width"] and 0 <= y < game_state["height"]}


def _adjacent_mines(game_state: dict, x: int, y: int) -> None:
    coords = _get_coords(game_state, x, y)

    return sum(game_state["squares"].get(dumps(coord)).get("is_mine") for coord in coords)


def _decrease_values(game_state: dict, x: int, y: int) -> int:
    mines = 0
    coords = _get_coords(game_state, x, y)

    for x, y in coords:
        square = game_state["squares"][dumps([x, y])]
        if square["is_mine"]:
            mines += 1
        elif square["adjacent_mines"] > 0:
            square["adjacent_mines"] -= 1

    return mines


def _reveal_zeros(game_state: dict, x: int, y: int, reveal_all: bool = True) -> None:
    if reveal_all or (not reveal_all and game_state["squares"][dumps([x, y])]["adjacent_mines"] == 0):
        game_state["squares"][dumps([x, y])]["is_open"] = True

    coords = _get_coords(game_state, x, y)

    for other_x, other_y in coords:
        square = game_state["squares"][dumps([other_x, other_y])]
        if not square["is_open"] and not square["is_mine"] and square["adjacent_mines"] == 0:
            _reveal_zeros(game_state, other_x, other_y)
        if reveal_all:
            square["is_open"] = True


def _remove_mines(game_state: dict, x: int, y: int):
    coords = _get_coords(game_state, x, y).union({(x, y)})

    for x, y in coords:
        square = game_state["squares"][dumps([x, y])]
        square["is_open"] = True
        if square["is_mine"]:
            square["is_mine"] = False
            _decrease_values(game_state, x, y)
            square["adjacent_mines"] = _adjacent_mines(game_state, x, y)


def square_clicked(game_state: dict, nickname: str, x: int, y: int) -> dict:
    square = game_state["squares"][dumps([x, y])]

    if not game_state["players"][nickname]["is_alive"]:
        return PlayerDead()
    elif not game_state["is_started"]:
        game_state["is_started"] = True
        _remove_mines(game_state, x, y)
        for x, y in _get_coords(game_state, x, y):
            if game_state["squares"][dumps([x, y])]["adjacent_mines"] == 0:
                _reveal_zeros(game_state, x, y)
            else:
                _reveal_zeros(game_state, x, y, False)
    elif game_state["squares"][dumps([x, y])]["is_mine"]:
        square["is_open"] = True
        eliminate_player(game_state, nickname)
        game_state["is_finished"] = True
        for player in game_state["players"]:
            if game_state["players"][player]["is_alive"]:
                game_state["is_finished"] = False
                break
    elif _is_won(game_state):
        game_state["is_finished"] = True
    else:
        square["is_open"] = True
        if square["adjacent_mines"] == 0:
            _reveal_zeros(game_state, x, y)

    return game_state


def _is_won(game_state: dict) -> True:
    squares = game_state["squares"]

    for coord in squares:
        if not squares[coord]["is_open"]:
            if not squares[coord]["is_mine"]:
                return False

    return True


def create_game(game_code: int, mines: int = 100, width: int = 30, height: int = 16):
    _mine_state = _generate_mines(mines, width, height)

    game_state = {
        "game_code": game_code,
        "is_started": False,
        "is_finished": False,
        "width": width,
        "height": height,
        "players": {},
        "squares": _mine_state,
    }

    for coord in _mine_state:
        value = _adjacent_mines(game_state, *_mine_state[coord]["coordinates"])
        game_state["squares"][coord]["adjacent_mines"] = value

    return game_state


def add_member_to_game(game_state: dict, nickname: str) -> None:
    if nickname in game_state["players"]:
        raise NicknameTaken()
    else:
        game_state["players"][nickname] = {"nickname": nickname, "is_alive": True}


def eliminate_player(game_state: dict, nickname: str) -> None:
    game_state["players"][nickname]["is_alive"] = False


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
