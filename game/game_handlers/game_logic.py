from random import randint


class NicknameTaken(ValueError):
    pass 


class PlayerDead(Exception):
    pass


def number_of_mines(width: int, height: int) -> int:

    lower = (width * height) // 5
    upper = (width * height) // 4
    return randint(lower, upper)


def _generate_mines(width: int, height: int, mines: int) -> dict:

    mine_squares = set()

    _mine_squares = {(x, y): {
            "coordinates": (x, y),
            "is_open": False,
            "is_mine": False,
            "adjacent_mines": 0
        }
        for y in range(height) for x in range(width)
    }

    for mine in range(mines):
        x, y = randint(0, width-1), randint(0, height-1)
        while (x, y) in mine_squares:
            x, y = randint(0, width-1), randint(0, height-1)
        mine_squares.add((x, y))
        _mine_squares[(x, y)]["is_mine"] = True

    return _mine_squares


def _adjacent_mines(game_state: dict, coordinate: tuple, width: int, height: int, change: bool) -> None:

    x, y = coordinate
    mines = 0

    for other_x in range(x-1, x+2):
        if 0 <= other_x < width:
            for other_y in range(y-1, y+2):
                if 0 <= other_y < height:
                    if (x != other_x or y != other_y):
                        if game_state["squares"][(other_x, other_y)]["is_mine"]:
                            mines += 1
                        elif change:
                            game_state["squares"][(other_x, other_y)]["adjacent_mines"] += 1
    
    return mines


def create_game(game_code: int, mines: int, width: int = 30, height: int = 16):

    _mine_state = _generate_mines(width, height, mines)

    game_state = {
        "game_code": game_code,
        "is_started": False,
        "players": {},
        "squares": _mine_state,
    }

    for (x, y) in _mine_state:
        value = _adjacent_mines(game_state, (x, y), width, height, False)
        game_state["squares"][(x, y)]["adjacent_mines"] = value

    return game_state
