from itertools import product
from json import dumps, loads
from random import choice, randint


class PlayerDead(Exception):
    """Handles what to do if a dead player clicks a square"""

    pass


class NicknameTaken(ValueError):
    """Handles what to do if a nickname is taken"""

    pass


class CommandFailed(ValueError):
    """Handles what to do if command function failed to operate"""

    pass


class NotPlayersTurn(ValueError):
    """Handles what to do if it's not the player's turn"""

    pass


class GameStarted(Exception):
    """Handles what to do if a player tries to join when the game has started"""

    pass


class GameFinished(Exception):
    """Handles what to do if a player tries to click a square when it has finished"""


def number_of_mines(width: int, height: int) -> int:
    """Calculates the number of mines there should be by the height and width"""
    lower = (width * height) // 5
    upper = (width * height) // 4
    return randint(lower, upper)


def _generate_mines(mines: int, width: int, height: int) -> dict:
    _mine_state = {
        dumps([x, y]): {"coordinates": (x, y), "is_open": False, "is_mine": False, "adjacent_mines": 0}
        for y in range(height)
        for x in range(width)
    }

    for mine in range(mines):
        x, y = randint(0, width - 1), randint(0, height - 1)
        while _mine_state[dumps([x, y])]["is_mine"]:
            x, y = randint(0, width - 1), randint(0, height - 1)
        _mine_state[dumps([x, y])]["is_mine"] = True

    return _mine_state


def _get_coords(game_state: dict, x: int, y: int) -> set:
    coords = set(product([x - 1, x, x + 1], [y - 1, y, y + 1])) - {(x, y)}
    return {(x, y) for (x, y) in coords if 0 <= x < game_state["width"] and 0 <= y < game_state["height"]}


def _adjacent_mines(game_state: dict, x: int, y: int) -> int:
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


def _assign_turn(game_state: dict, nickname: str) -> None:

    players = game_state["players"]
    alive_players = [player for player in players if players[player]["is_alive"]]

    if len(alive_players) != 1:
        current_player_index = alive_players.index(nickname)

        if current_player_index == len(alive_players) - 1:
            next_player = alive_players[0]
        else:
            next_player = alive_players[current_player_index + 1]

        game_state["turn_id"] = players[next_player]["id"]

    else:
        game_state["turn_id"] = players[nickname]["id"]


def square_clicked(game_state: dict, nickname: str, x: int, y: int) -> dict:

    if not game_state["players"][nickname]["is_alive"]:
        raise PlayerDead()
    elif game_state["is_finished"]:
        raise GameFinished()
    elif game_state["turn_id"] != game_state["players"][nickname]["id"]:
        raise NotPlayersTurn()

    _assign_turn(game_state, nickname)

    square = game_state["squares"][dumps([x, y])]

    if not game_state["is_started"]:
        _remove_mines(game_state, x, y)
        for x, y in _get_coords(game_state, x, y):
            if game_state["squares"][dumps([x, y])]["adjacent_mines"] == 0:
                _reveal_zeros(game_state, x, y, reveal_all=True)
            else:
                _reveal_zeros(game_state, x, y, reveal_all=False)
    elif game_state["squares"][dumps([x, y])]["is_mine"]:
        square["is_open"] = True
        eliminate_player(game_state, nickname)
        game_state["is_finished"] = True
        for player in game_state["players"]:
            if game_state["players"][player]["is_alive"]:
                game_state["is_finished"] = False
                break

    square["is_open"] = True

    if _is_won(game_state):
        print("WON")
        game_state["is_finished"] = True
    elif square["adjacent_mines"] == 0 and game_state["is_started"] and not square["is_mine"]:
        _reveal_zeros(game_state, x, y)

    if not game_state["is_started"]:
        game_state["is_started"] = True

    return game_state


def _is_won(game_state: dict) -> bool:
    squares = game_state["squares"]

    for coord in squares:
        if not squares[coord]["is_open"]:
            if not squares[coord]["is_mine"]:
                return False

    return True


def delete_square(game_state: dict, nickname: str) -> dict:

    if game_state["players"][nickname]["squares_deleted"] == 5:
        return game_state

    game_state["players"][nickname]["squares_deleted"] += 1
    squares = game_state["squares"]
    safe_squares = [square for square in squares if not squares[square]["is_mine"]]
    closed_squares = [square for square in safe_squares if not squares[square]["is_open"]]
    deleted_square = choice(closed_squares)

    square_clicked(game_state, nickname, *loads(deleted_square))

    return game_state


def roll_winner(game_state: dict, nickname: str) -> dict:
    players = game_state["players"]

    if players[nickname]["chanced_win"] or nickname not in players or not players[nickname]["is_alive"]:
        return game_state

    alive_players = [player for player in players if players[player]["is_alive"]]
    chancing_players = [player for player in alive_players if not players[player]["chanced_win"]]
    chance = randint(1, len(chancing_players) * 2)

    players[nickname]["chanced_win"] = True

    if chance == 1:
        for player in alive_players:
            if nickname != player:
                game_state["players"][player]["is_alive"] = False

    _assign_turn(game_state, nickname)

    return game_state


def new_life(game_state: dict, nickname: str) -> dict:

    players = game_state["players"]

    if not players[nickname]["is_alive"] and not players[nickname]["revived"]:
        players[nickname]["revived"] = True
        if randint(1, len(players)) == 1:
            game_state["players"][nickname]["is_alive"] = True
            game_state["is_finished"] = False

    alive_players = [player for player in players if players[player]["is_alive"]]

    if len(alive_players) == 1 and players[nickname]["is_alive"]:
        game_state["turn_id"] = players[nickname]["id"]

    return game_state


def close_open_squares(game_state: dict, nickname: str) -> dict:

    if game_state["closed_used"] or game_state["players"][nickname]["is_alive"]:
        return game_state

    game_state["closed_used"] = True
    squares = game_state["squares"]

    for square in game_state["squares"]:
        if squares[square]["is_open"]:
            game_state["squares"][square]["is_open"] = False

    return game_state


def create_game(game_code: int, mines: int = 100, width: int = 30, height: int = 16):
    _mine_state = _generate_mines(mines, width, height)

    game_state = {
        "game_code": game_code,
        "is_started": False,
        "is_finished": False,
        "turn_id": 1,
        "closed_used": False,
        "width": width,
        "height": height,
        "players": {},
        "squares": _mine_state
    }

    for coord in _mine_state:
        value = _adjacent_mines(game_state, *_mine_state[coord]["coordinates"])
        game_state["squares"][coord]["adjacent_mines"] = value

    return game_state


def add_member_to_game(game_state: dict, nickname: str) -> None:

    if game_state["is_started"]:
        raise GameStarted()
    elif nickname in game_state["players"]:
        raise NicknameTaken()

    game_state["players"][nickname] = {
        "id": len(game_state["players"]) + 1,
        "nickname": nickname,
        "is_alive": True,
        "chanced_win": False,
        "revived": False,
        "squares_deleted": 0,
    }


def eliminate_player(game_state: dict, nickname: str) -> None:

    game_state["players"][nickname]["is_alive"] = False
