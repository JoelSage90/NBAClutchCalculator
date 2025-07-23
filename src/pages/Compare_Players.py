# streamlit_app.py
# Page Title: Compare Players
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


from display_clutchness import display_clutchness,compare_clutchness


st.title("NBA Clutchness Comparer")
st.subheader("Select 2 players and compare clutch they are")
player_list = pd.read_csv("/data/players.csv")
select_col1,select_col2 = st.columns(2)
cached_players = ["Kevin Durant","Stephen Curry", "LeBron James"]
with select_col1:
    player1 = st.selectbox("Select Player 1",player_list["PLAYER"].unique(), index= None)

with select_col2:
    player2 = st.selectbox("Select Player 2",player_list["PLAYER"].unique(), index= None)

if player1 is not None and player2 is not None:
    col1, col2 = st.columns(2)
    with col1:
        compare_clutchness(player1, player_list, cached_players)
    with col2:
        compare_clutchness(player2, player_list, cached_players)   