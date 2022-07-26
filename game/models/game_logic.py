# models/game_logic.py

def number_of_mines() -> int:
    ...


def _generate_mines(width: int, height: int, mines: int):
    ...


def create_game(game_code: int, mines: int, width: int = 20, height: int = 50):
    mine_state = _generate_mines(width, height, mines)
    game_state = {
        game_code: int,
        "is_started": bool,
        "players": [],
        "squares": mine_state,
    }

    return game_state
