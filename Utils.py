# utils.py
"""Utility functions and constants for the Streamlit Snake and Ladder game."""

import random
from typing import Dict, Tuple

BOARD_SIZE = 100
BOARD_DIM = 10

SNAKES: Dict[int, int] = {
    99: 78, 95: 75, 92: 88, 89: 53, 74: 34,
    64: 60, 62: 19, 49: 11, 46: 25, 16: 6,
}

LADDERS: Dict[int, int] = {
    2: 38, 7: 14, 8: 31, 15: 26, 21: 42,
    28: 84, 36: 44, 51: 67, 71: 91, 78: 98, 87: 94,
}

PLAYER_ICONS = ["🔴", "🔵", "🟢", "🟡", "🟣", "🟠"]


def roll_dice() -> int:
    return random.randint(1, 6)


def move_player(position: int, roll: int) -> Tuple[int, str]:
    tentative = position + roll
    if tentative > BOARD_SIZE:
        return position, "🎯 Almost there! Need exact roll to reach 100."

    new_pos = tentative
    if new_pos in LADDERS:
        final_pos = LADDERS[new_pos]
        return final_pos, f"🪜 Ladder! Climbed from {new_pos} to {final_pos}!"
    if new_pos in SNAKES:
        final_pos = SNAKES[new_pos]
        return final_pos, f"🐍 Snake! Slid from {new_pos} down to {final_pos}!"
    return new_pos, ""


def format_cell(cell_num: int, player_positions: Dict[str, int], player_icons: Dict[str, str]) -> str:
    token = ""
    for player, pos in player_positions.items():
        if pos == cell_num:
            token += player_icons[player]
    extra = ""
    if cell_num in SNAKES:
        extra = f"🐍→{SNAKES[cell_num]}"
    if cell_num in LADDERS:
        extra = f"🪜→{LADDERS[cell_num]}"
    parts = [str(cell_num)]
    if token:
        parts.append(token)
    if extra:
        parts.append(extra)
    return "<br>".join(parts)


def initialize_game_state(num_players: int = 2, names: list = None) -> Dict:
    if names is None or len(names) != num_players:
        names = [f"Player {i+1}" for i in range(num_players)]
    players = [f"player{i+1}" for i in range(num_players)]
    positions = {p: 0 for p in players}
    icons = {p: PLAYER_ICONS[i] for i, p in enumerate(players)}
    display_names = {p: names[i] for i, p in enumerate(players)}
    return {
        "players": players,
        "positions": positions,
        "icons": icons,
        "names": display_names,
        "turn_index": 0,
        "dice": 0,
        "history": [],
        "dice_history": [],
        "winner": None,
        "extra_turn": False,
    }


def record_move(state: Dict, player: str, roll: int, message: str, pos_before: int, pos_after: int) -> None:
    name = state["names"][player]
    entry = f"{name} rolled {roll}. Moved from {pos_before} to {pos_after}. {message}"
    state["history"].append(entry)
    state["dice_history"].append(roll)

# End of utils.py
