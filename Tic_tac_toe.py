import streamlit as st import numpy as np import time import base64

st.set_page_config(page_title="Tic Tac Toe", layout="centered")

Styling

st.markdown(""" <style> .main { background-color: black; } .block-container { padding-top: 2rem; } .title { color: white; text-align: center; font-size: 40px; } .winner { color: gold; text-align: center; font-size: 30px; } </style> """, unsafe_allow_html=True)

st.markdown('<div class="title">Tic Tac Toe</div>', unsafe_allow_html=True)

Load sounds

win_sound = """ data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAESsAACJWAAACABAAZGF0YcQAAAAA/////wD///8A////AP///wD///8A////AP///wD///8A"""  # short click click_sound = """ data:audio/wav;base64,UklGRkQAAABXQVZFZm10IBAAAAABAAEAIlYAAESsAAACABAAZGF0YcQAAAAA/////wD///8A////AP///wD///8A////AP///wD///8A"""  # short click

def play_sound(sound): st.markdown(f""" <audio autoplay> <source src="{sound}" type="audio/wav"> </audio> """, unsafe_allow_html=True)

Game state

if 'board' not in st.session_state: st.session_state.board = ["" for _ in range(9)] st.session_state.current_player = "X" st.session_state.winner = None st.session_state.scores = {"X": 0, "O": 0}

def check_winner(): b = st.session_state.board lines = [ [b[0], b[1], b[2]], [b[3], b[4], b[5]], [b[6], b[7], b[8]],  # rows [b[0], b[3], b[6]], [b[1], b[4], b[7]], [b[2], b[5], b[8]],  # cols [b[0], b[4], b[8]], [b[2], b[4], b[6]]  # diags ] for line in lines: if line[0] == line[1] == line[2] and line[0] != "": return line[0] return None

def reset_game(): st.session_state.board = ["" for _ in range(9)] st.session_state.current_player = "X" st.session_state.winner = None

Score tracker

st.markdown("""

<div style='text-align:center; color:white; font-size:20px;'>
    Score - X: {x} | O: {o}
</div>
""".format(x=st.session_state.scores['X'], o=st.session_state.scores['O']), unsafe_allow_html=True)cols = st.columns(3) for i in range(3): for j in range(3): idx = i * 3 + j with cols[j]: if st.session_state.board[idx] == "" and st.session_state.winner is None: if st.button(" ", key=idx, help=f"Cell {i+1},{j+1}", use_container_width=True): st.session_state.board[idx] = st.session_state.current_player play_sound(click_sound) st.session_state.winner = check_winner() if st.session_state.winner: play_sound(win_sound) st.session_state.scores[st.session_state.winner] += 1 else: st.session_state.current_player = "O" if st.session_state.current_player == "X" else "X" else: color = "gold" if st.session_state.board[idx] == st.session_state.winner else "white" st.markdown(f"<div style='border:1px solid white; color:{color}; text-align:center; padding:20px;'>{st.session_state.board[idx]}</div>", unsafe_allow_html=True)

if st.session_state.winner: st.markdown(f"<div class='winner'>{st.session_state.winner} wins!</div>", unsafe_allow_html=True)

if st.button("Reset Game"): reset_game()


