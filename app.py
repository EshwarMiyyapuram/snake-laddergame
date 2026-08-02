# app.py
"""Streamlit Snake & Ladder — 2 to 6 players, extra turn on 6, custom names,
snake/ladder destination shown on board, side dice panel, winner announcement."""

import streamlit as st
from Utils import (
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
# Setup screen (choose number of players + names) before game starts
# -------------------------------------------------------------------
if "game" not in st.session_state:
    st.session_state["setup_done"] = False

if not st.session_state.get("setup_done", False):
    st.markdown("<h1 style='text-align:center;'>🐍 Snake & Ladder Setup 🪜</h1>", unsafe_allow_html=True)
    st.write("Choose number of players and enter their names.")

    num_players = st.selectbox("Number of Players", [2, 3, 4, 5, 6], index=0)

    names = []
    cols = st.columns(num_players)
    for i in range(num_players):
        with cols[i]:
            default = f"Player {i+1}"
            n = st.text_input(f"Name {i+1}", value=default, key=f"name_input_{i}")
            names.append(n.strip() if n.strip() else default)

    if st.button("🚀 Start Game"):
        st.session_state["game"] = initialize_game_state(num_players, names)
        st.session_state["setup_done"] = True
        st.rerun()

    st.stop()

state = st.session_state["game"]

# -------------------------------------------------------------------
# Helper: display the board
# -------------------------------------------------------------------
def display_board():
    for row_idx in reversed(range(BOARD_DIM)):
        start = row_idx * BOARD_DIM + 1
        end = start + BOARD_DIM - 1
        if row_idx % 2 == 0:
            numbers = list(range(start, end + 1))
        else:
            numbers = list(reversed(range(start, end + 1)))
        cols = st.columns(BOARD_DIM)
        for col, cell_num in zip(cols, numbers):
            cell_content = format_cell(cell_num, state["positions"], state["icons"])
            col.markdown(
                f"<div class='cell'>{cell_content}</div>",
                unsafe_allow_html=True,
            )

# -------------------------------------------------------------------
# Sidebar
# -------------------------------------------------------------------
st.sidebar.title("🐍 Snake & Ladder")
with st.sidebar.expander("📝 Game Rules"):
    st.write(
        "* Players start off the board (position 0).\n"
        "* Roll the dice (1‑6) and move forward.\n"
        "* Rolling a **6** gives you an extra turn!\n"
        "* Landing on a **ladder** climbs you up.\n"
        "* Landing on a **snake** slides you down.\n"
        "* You must land **exactly** on 100 to win.\n"
        "* First player to reach 100 wins!"
    )
if st.sidebar.button("🔄 Restart / New Game"):
    st.session_state.pop("game", None)
    st.session_state["setup_done"] = False
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
        padding: 4px;
        height: 70px;
        width: 70px;
        text-align: center;
        font-size: 0.75rem;
        background: #f9f9f9;
        color: #111;
        display: flex;
        flex-direction: column;
        justify-content: center;
        line-height: 1.1;
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
    .stButton>button:hover { filter: brightness(1.1); }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='title'>🐍 Snake & Ladder 🪜</div>", unsafe_allow_html=True)

# -------------------------------------------------------------------
# Winner banner
# -------------------------------------------------------------------
if state["winner"]:
    winner_name = state["names"][state["winner"]]
    winner_icon = state["icons"][state["winner"]]
    st.success(f"🎉 {winner_icon} {winner_name} wins the game! 🎉")

# -------------------------------------------------------------------
# Main layout
# -------------------------------------------------------------------
board_col, side_col = st.columns([3, 1])

with side_col:
    st.markdown("### 🎯 Status")
    for p in state["players"]:
        st.metric(f"{state['icons'][p]} {state['names'][p]}", state["positions"][p])

    current_player = state["players"][state["turn_index"]]
    current_name = state["names"][current_player]
    current_icon = state["icons"][current_player]
    st.markdown(f"**Turn: {current_icon} {current_name}**")

    st.markdown("---")
    st.markdown(f"### Dice: {state['dice']} 🎲")

    if st.button("Roll Dice 🎲") and not state["winner"]:
        roll = roll_dice()
        state["dice"] = roll

        old_pos = state["positions"][current_player]
        new_pos, message = move_player(old_pos, roll)
        state["positions"][current_player] = new_pos
        record_move(state, current_player, roll, message, old_pos, new_pos)

        if new_pos == BOARD_SIZE:
            state["winner"] = current_player
            st.balloons()
        else:
            if roll == 6:
                # extra turn: same player goes again
                state["extra_turn"] = True
            else:
                state["extra_turn"] = False
                state["turn_index"] = (state["turn_index"] + 1) % len(state["players"])
        st.rerun()

    if state.get("extra_turn") and not state["winner"]:
        st.info(f"🎲 Rolled a 6! {current_name} gets another turn!")

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
# Footer
# -------------------------------------------------------------------
move_counts = " | ".join(
    f"{state['icons'][p]} {state['names'][p]} moves: "
    f"{sum(1 for h in state['history'] if h.startswith(state['names'][p]))}"
    for p in state["players"]
)
st.caption(move_counts)

# End of app.py
