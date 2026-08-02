# app.py
"""Streamlit implementation of a two‑player Snake and Ladder game.

Features:
- 10×10 board visualised with emojis and numbers
- Two players (🔴 Player 1, 🔵 Player 2)
- Roll dice button (random 1‑6)
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
    # Create rows from top (row index 9) down to 0
    for row_idx in reversed(range(BOARD_DIM)):
        # Determine the numbers for this row
        start = row_idx * BOARD_DIM + 1
        end = start + BOARD_DIM - 1
        # Serpentine direction: even rows (from bottom) go left→right,
        # odd rows go right→left.
        if row_idx % 2 == 0:
            numbers = list(range(start, end + 1))
        else:
            numbers = list(reversed(range(start, end + 1)))
        cols = st.columns(BOARD_DIM)
        for col, cell_num in zip(cols, numbers):
            cell_content = format_cell(cell_num, player_positions)
            # Use a markdown card style for each cell
            col.markdown(
                f"""
                <div class='cell'>
                {cell_content}
                </div>
                """,
                unsafe_allow_html=True,
            )

# -------------------------------------------------------------------
# UI – Sidebar
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
# Restart button (sidebar)
if st.sidebar.button("🔄 Restart Game"):
    st.session_state["game"] = initialize_game_state()
    st.rerun()

# -------------------------------------------------------------------
# Custom CSS for a modern look
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
    }
    .stButton>button:hover {
        filter: brightness(1.1);
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
# Scoreboard and turn indicator
# -------------------------------------------------------------------
col1, col2, col3 = st.columns([2, 2, 2])
with col1:
    st.metric("🔴 Player 1", state["player1"])
with col2:
    st.metric("🔵 Player 2", state["player2"])
with col3:
    turn_name = "🔴 Player 1" if state["turn"] == "player1" else "🔵 Player 2"
    st.metric("Turn", turn_name)

# -------------------------------------------------------------------
# Dice display and Roll button
# -------------------------------------------------------------------
st.subheader(f"Dice: {state['dice']} 🎲")
if st.button("Roll Dice 🎲") and not state["winner"]:
    roll = roll_dice()
    state["dice"] = roll
    # Apply move for the current player
    old_pos = state[state["turn"]]
    new_pos, message = move_player(old_pos, roll)
    state[state["turn"]] = new_pos
    # Record the move (pass explicit before/after positions)
    record_move(state, roll, message, old_pos, new_pos)
    # Check for win condition
    if new_pos == BOARD_SIZE:
        state["winner"] = state["turn"]
        st.success(f"{turn_name} wins! 🎉")
        st.balloons()
    else:
        # Switch turn only if game not over
        state["turn"] = "player2" if state["turn"] == "player1" else "player1"
    st.rerun()

# -------------------------------------------------------------------
# History panels
# -------------------------------------------------------------------
st.subheader("🕹️ Move History")
if state["history"]:
    for entry in reversed(state["history"][-10:]):  # show last 10 moves
        st.write(entry)
else:
    st.write("No moves yet. Roll the dice to start!")

# -------------------------------------------------------------------
# Board rendering
# -------------------------------------------------------------------
st.subheader("🎲 Game Board")
display_board()

# -------------------------------------------------------------------
# Footer – number of moves per player
# -------------------------------------------------------------------
player1_moves = sum(1 for h in state["history"] if h.startswith("Player1"))
player2_moves = sum(1 for h in state["history"] if h.startswith("Player2"))
st.caption(f"🔴 Player 1 moves: {player1_moves} | 🔵 Player 2 moves: {player2_moves}")

# End of app.py
