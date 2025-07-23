# streamlit_app.py
# Page Title: Clutchness calculator
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamviz import gauge

from collect_data import get_career_shot_data
from shot_plot import draw_heat_map
from clutch_score import clutchness_calculator
from display_clutchness import display_clutchness

st.set_page_config(layout="wide")


st.title("NBA Clutchness Calculator")
st.subheader("Select a player and see how clutch they are")
player_list = pd.read_csv("/data/players.csv")
player = st.selectbox("select a player",player_list["PLAYER"].unique(), index= None)

#check for players who are already saved rather than making an api call
cached_players = ["Kevin Durant","Stephen Curry", "LeBron James"]
col1,col2 = st.columns([1,1.1])

display_clutchness(player,col1,col2,player_list,cached_players)
