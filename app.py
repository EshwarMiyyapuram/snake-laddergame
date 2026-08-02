# app.py
"""Streamlit implementation of a two‑player Snake and Ladder game.

Features:
- 10×10 board visualised with emojis and numbers
- Two players (🔴 Player 1, 🔵 Player 2)
- Roll dice button (random 1‑6) — now in a side panel next to the board
- Automatic movement respecting snakes, ladders and exact‑100 rule
- Turn indicator, dice display, move history, and score board
- Celebration with Streamlit balloons when someone wins
- Restart button to start a fresh game
- Sidebar with rules, "About" and a reset button
- Custom CSS for a modern, colourful UI
"""

import streamlit as st
from utils import (
    BOARD_SIZE,
    BOARD_DIM,
    SNAKES,
    LADDERS,
    roll_dice,
    move_player,
    format_cell,
    initialize_game_state,
    record_move,
)

st.set_page_config(layout="wide")

# -------------------------------------------------------------------
# Session state initialisation
# -------------------------------------------------------------------
if "game" not in st.session_state:
    st.session_state["game"] = initialize_game_state()

state = st.session_state["game"]

# -------------------------------------------------------------------
# Helper: display the board (10×10 grid)
# -------------------------------------------------------------------
def display_board():
    """Render the board using Streamlit columns.

    The board follows the classic serpentine numbering:
    - Row 1 (bottom) left → right (1‑10)
    - Row 2 right → left (11‑20)
    - … and so on up to 100 at the top left.
    """
    player_positions = {"player1": state["player1"], "player2": state["player2"]}
    for row_idx in reversed(range(BOARD_DIM)):
        start = row_idx * BOARD_DIM + 1
        end = start + BOARD_DIM - 1
        if row_idx % 2 == 0:
            numbers = list(range(start, end + 1))
        else:
            numbers = list(reversed(range(start, end + 1)))
        cols = st.columns(BOARD_DIM)
        for col, cell_num in zip(cols, numbers):
            cell_content = format_cell(cell_num, player_positions)
            col.markdown(
                f"""
                <div class='cell'>
                {cell_content}
                </div>
                """,
                unsafe_allow_html=True,
            )

# -------------------------------------------------------------------
# UI – Sidebar (rules / about / restart)
# -------------------------------------------------------------------
st.sidebar.title("🐍 Snake & Ladder")
with st.sidebar.expander("📝 Game Rules"):
    st.write(
        "* Two players start off the board (position 0).\n"
        "* Roll the dice (1‑6) and move forward.\n"
        "* Landing on a **ladder** climbs you up.\n"
        "* Landing on a **snake** slides you down.\n"
        "* You must land **exactly** on 100 to win – overshoot means you stay still.\n"
        "* First player to reach 100 wins!"
    )
with st.sidebar.expander("ℹ️ About the Game"):
    st.write(
        "A simple, beginner‑friendly implementation built with Python 3 and Streamlit. "
        "No backend, no database – everything lives in the browser session."
    )
if st.sidebar.button("🔄 Restart Game"):
    st.session_state["game"] = initialize_game_state()
    st.rerun()

# -------------------------------------------------------------------
# Custom CSS
# -------------------------------------------------------------------
st.markdown(
    """
    <style>
    .title {
        background: linear-gradient(90deg, #ff7e5f, #feb47b);
        -webkit-background-clip: text;
        color: transparent;
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .cell {
        border: 1px solid #ddd;
        border-radius: 4px;
        padding: 6px;
        height: 60px;
        width: 60px;
        text-align: center;
        font-size: 0.9rem;
        background: #f9f9f9;
    }
    .stButton>button {
        background: linear-gradient(90deg, #36d1dc, #5b86e5);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        width: 100%;
    }
    .stButton>button:hover {
        filter: brightness(1.1);
    }
    .side-panel {
        background: #1a1c24;
        border-radius: 10px;
        padding: 1rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------------
# Main title
# -------------------------------------------------------------------
st.markdown("<div class='title'>🐍 Snake & Ladder 🪜</div>", unsafe_allow_html=True)

# -------------------------------------------------------------------
# Main layout: board on the left, dice/controls/scoreboard on the right
# -------------------------------------------------------------------
board_col, side_col = st.columns([3, 1])

with side_col:
    st.markdown("### 🎯 Status")

    turn_name = "🔴 Player 1" if state["turn"] == "player1" else "🔵 Player 2"
    st.metric("🔴 Player 1", state["player1"])
    st.metric("🔵 Player 2", state["player2"])
    st.metric("Turn", turn_name)

    st.markdown("---")
    st.markdown(f"### Dice: {state['dice']} 🎲")

    if st.button("Roll Dice 🎲") and not state["winner"]:
        roll = roll_dice()
        state["dice"] = roll
        old_pos = state[state["turn"]]
        new_pos, message = move_player(old_pos, roll)
        state[state["turn"]] = new_pos
        record_move(state, roll, message, old_pos, new_pos)
        if new_pos == BOARD_SIZE:
            state["winner"] = state["turn"]
            st.success(f"{turn_name} wins! 🎉")
            st.balloons()
        else:
            state["turn"] = "player2" if state["turn"] == "player1" else "player1"
        st.rerun()

    st.markdown("---")
    st.markdown("### 🕹️ Move History")
    if state["history"]:
        for entry in reversed(state["history"][-8:]):
            st.caption(entry)
    else:
        st.caption("No moves yet. Roll the dice to start!")

with board_col:
    st.subheader("🎲 Game Board")
    display_board()

# -------------------------------------------------------------------
# Footer – number of moves per player
# -------------------------------------------------------------------
player1_moves = sum(1 for h in state["history"] if h.startswith("Player1"))
player2_moves = sum(1 for h in state["history"] if h.startswith("Player2"))
st.caption(f"🔴 Player 1 moves: {player1_moves} | 🔵 Player 2 moves: {player2_moves}")

# End of app.py
