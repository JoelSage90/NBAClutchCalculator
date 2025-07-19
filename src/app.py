import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from streamviz import gauge

from collect_data import get_career_shot_data
from shot_plot import draw_heat_map
from clutch_score import clutchness_calculator
def clutch_shooting(data):
    total_made = 0
    total_attempts = 0
    highest_fgp_section = None
    highest_fgp = 0

    for section, stats in data.items():
        fgp, made, attempted = stats
        total_made += made
        total_attempts += attempted

        if fgp > highest_fgp:
            highest_fgp = fgp
            highest_fgp_section = section

    overall_fgp = total_made / total_attempts if total_attempts else 0
    return highest_fgp_section,highest_fgp,overall_fgp

st.set_page_config(layout="wide")


st.title("NBA Clutchness Calculator")
st.subheader("Select a player and see how clutch they are")
player_list = pd.read_csv("../data/players.csv")
player = st.selectbox("select a player",player_list["PLAYER"].unique(), index= None)

#check for players who are already saved rather than making an api call
cached_players = ["Kevin Durant","Stephen Curry", "LeBron James"]
col1,col2 = st.columns([1,1.1])
if player is not None:
    if player in cached_players:
        filename = "../data/"+player.replace(" ", "_") + "_clutch.csv"
        player_id = player_list.loc[player_list["PLAYER"] == player, "PLAYER_ID"].values[0]
        player_df = pd.read_csv(filename)
    else:
        #wait for the api call to finish
        with st.spinner("Fetching data from NBA API..."):
            player_id = player_list.loc[player_list["PLAYER"] == player, "PLAYER_ID"].values[0]
            player_df = get_career_shot_data(player_id)
    #plot the clutch shots
    fig,ax,section_percentage = draw_heat_map(player_df)
    section,section_fgp,overall = clutch_shooting(section_percentage)
    with col1:
        st.pyplot(fig)
    with col2:
        st.markdown("### Player Info")
        nested_col1, nested_col2 = st.columns(2)
        
        with nested_col1:
            img_url = f"https://cdn.nba.com/headshots/nba/latest/260x190/{player_id}.png"
            st.image(img_url, width=300)
        with nested_col2:
            clutchness = clutchness_calculator(player_df)
            st.markdown(f"**Player Name:** {player}")
            st.markdown(f"**Overall fgp:** {overall:.3f}")
            st.markdown(f"**Best Section:** {section} {section_fgp:.3f}")
            print(section_percentage)
        clutchness = clutchness_calculator(player_df)
        #change formatting for this
        
        gauge(gVal=(clutchness/100),
              gTitle="Clutchness",
              grLow=0.5,
              grMid=0.6,
              gTheme= "White")

        
else:
    st.info("Select a player to see how clutch they are.")
