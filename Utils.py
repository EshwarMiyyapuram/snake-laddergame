# utils.py
"""Utility functions and constants for the Streamlit Snake and Ladder game.

This file contains:
- board dimensions
- snake and ladder mappings
- helper functions for dice roll, movement, and messages

The code is intentionally simple and heavily commented to be beginner‑friendly.
"""

import random
from typing import Dict, Tuple, List

# ------------------------------------------------------------
# Board configuration
# ------------------------------------------------------------
BOARD_SIZE = 100  # total cells (10x10)
BOARD_DIM = 10    # width and height of the grid

# Snakes: key = head (higher number), value = tail (lower number)
# Example positions – you can customise as desired
SNAKES: Dict[int, int] = {
    99: 78,
    95: 75,
    92: 88,
    89: 53,
    74: 34,
    64: 60,
    62: 19,
    49: 11,
    46: 25,
    16: 6,
}

# Ladders: key = bottom (lower number), value = top (higher number)
LADDERS: Dict[int, int] = {
    2: 38,
    7: 14,
    8: 31,
    15: 26,
    21: 42,
    28: 84,
    36: 44,
    51: 67,
    71: 91,
    78: 98,
    87: 94,
}

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def roll_dice() -> int:
    """Return a random integer between 1 and 6 inclusive."""
    return random.randint(1, 6)


def move_player(position: int, roll: int) -> Tuple[int, str]:
    """Calculate the new position after a dice roll.

    Args:
        position: Current cell number (1‑100). 0 means "not yet on the board".
        roll: Dice value (1‑6).

    Returns:
        A tuple of (new_position, message) where *message* explains any
        special event (snake bite, ladder climb, overshoot, etc.).
    """
    tentative = position + roll
    # Overshoot rule – must land exactly on 100
    if tentative > BOARD_SIZE:
        return position, "🎯 Almost there! Need exact roll to reach 100."

    # Normal move
    new_pos = tentative
    # Check for ladders first (climb up)
    if new_pos in LADDERS:
        final_pos = LADDERS[new_pos]
        return final_pos, "🪜 Great! You climbed a ladder!"
    # Then snakes (slide down)
    if new_pos in SNAKES:
        final_pos = SNAKES[new_pos]
        return final_pos, "🐍 Oops! A snake bit you!"
    return new_pos, ""


def format_cell(cell_num: int, player_positions: Dict[str, int]) -> str:
    """Return a string representation of a board cell.

    The cell shows its number and any player tokens that currently occupy it.
    Player 1 uses 🔴, Player 2 uses 🔵.
    """
    token = ""
    for player, pos in player_positions.items():
        if pos == cell_num:
            token += "🔴" if player == "player1" else "🔵"
    # Show snake or ladder icons on the static board
    if cell_num in SNAKES:
        token += "🐍"
    if cell_num in LADDERS:
        token += "🪜"
    return f"{cell_num}\n{token}" if token else str(cell_num)


def initialize_game_state() -> Dict:
    """Create a fresh session_state dictionary for a new game.

    Returns a dict that can be stored directly in ``st.session_state``.
    """
    return {
        "player1": 0,  # start off the board (position 0)
        "player2": 0,
        "turn": "player1",
        "dice": 0,
        "history": [],  # list of strings describing each move
        "dice_history": [],  # list of ints
        "winner": None,
    }


def record_move(state: Dict, roll: int, message: str) -> None:
    """Append a textual description of the most recent turn to the history.

    The function mutates the provided *state* dictionary.
    """
    player = state["turn"]
    pos_before = state[player]
    # After movement the state already contains the new position
    pos_after = state[player]
    entry = (
        f"{player.title()} rolled {roll}. "
        f"Moved from {pos_before} to {pos_after}. "
        f"{message}"
    )
    state["history"].append(entry)
    state["dice_history"].append(roll)

# End of utils.py
