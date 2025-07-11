import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from collect_data import get_career_shot_data
from shot_plot import draw_heat_map
from clutch_score import clutchness_calculator

st.set_page_config(layout="wide")
st.title("NBA Clutchness Calculator")
st.subheader("Select a player and see how clutch they are")
player_list = pd.read_csv("../data/players.csv")
player = st.selectbox("select a player",player_list["PLAYER"].unique(), index= None)

#check for players who are already saved rather than making an api call
cached_players = ["Kevin Durant","Stephen Curry", "LeBron James"]
col1,col2 = st.columns([2,1])
if player is not None:
    if player in cached_players:
        filename = "../data/"+player.replace(" ", "_") + "_clutch.csv"
        player_df = pd.read_csv(filename)
    else:
        #wait for the api call to finish
        with st.spinner("Fetching data from NBA API..."):
            player_id = player_list.loc[player_list["PLAYER"] == player, "PLAYER_ID"].values[0]
            player_df = get_career_shot_data(player_id)

    #plot the clutch shots
    with col1:
        fig,ax = draw_heat_map(player_df)
        st.pyplot(fig)
    with col2:
        clutchness = clutchness_calculator(player_df)
        st.markdown("### Player Info")
        st.markdown(f"**Player Name:** {player}")
        st.markdown(f"Clutchness: {clutchness:.2f}")

else:
    st.info("Select a player to see how clutch they are.")
