import streamlit as st
import numpy as np
import time

# Set up page configuration
st.set_page_config(page_title="Tic Tac Toe", layout="centered")

# Custom CSS styling
st.markdown("""
    <style>
        .main {
            background-color: black;
        }
        .block-container {
            padding-top: 2rem;
        }
        .title {
            color: white;
            text-align: center;
            font-size: 40px;
        }
        .winner {
            color: gold;
            text-align: center;
            font-size: 30px;
        }
        .draw {
            color: gray;
            text-align: center;
            font-size: 25px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">Tic Tac Toe</div>', unsafe_allow_html=True)

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = ["" for _ in range(9)]
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.scores = {"X": 0, "O": 0}
    st.session_state.game_over = False

# Load and prepare audio
click_audio = open("click.wav", "rb")
win_audio = open("win.wav", "rb")

def check_winner():
    b = st.session_state.board
    lines = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]
    for line in lines:
        if b[line[0]] == b[line[1]] == b[line[2]] and b[line[0]] != "":
            return b[line[0]], line
    return None, []

def is_draw():
    return all(cell != "" for cell in st.session_state.board) and not st.session_state.winner

def reset_game():
    st.session_state.board = ["" for _ in range(9)]
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.game_over = False

# Score display
st.markdown(f"""
<div style='text-align:center; color:white; font-size:20px;'>
    Score - X: {st.session_state.scores['X']} | O: {st.session_state.scores['O']}
</div>
""", unsafe_allow_html=True)

# Game grid
cols = st.columns(3)
win_line = []
for i in range(3):
    for j in range(3):
        idx = i * 3 + j
        with cols[j]:
            cell_value = st.session_state.board[idx]
            if cell_value == "" and not st.session_state.game_over:
                if st.button(" ", key=idx, use_container_width=True):
                    st.session_state.board[idx] = st.session_state.current_player
                    st.audio(click_audio, format='audio/wav')
                    winner, win_line = check_winner()
                    if winner:
                        st.session_state.winner = winner
                        st.session_state.scores[winner] += 1
                        st.session_state.game_over = True
                        st.audio(win_audio, format='audio/wav')
                    elif is_draw():
                        st.session_state.game_over = True
                    else:
                        st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X"
            else:
                cell_color = "gold" if idx in win_line else "white"
                st.markdown(f"<div style='border:1px solid white; color:{cell_color}; text-align:center; padding:20px; font-size:24px'>{cell_value}</div>", unsafe_allow_html=True)

# Outcome display
if st.session_state.winner:
    st.markdown(f"<div class='winner'>{st.session_state.winner} wins!</div>", unsafe_allow_html=True)
elif st.session_state.game_over:
    st.markdown(f"<div class='draw'>It's a draw!</div>", unsafe_allow_html=True)

# Reset game
if st.button("Reset Game"):
    reset_game()
