from nba_api.stats.endpoints import shotchartdetail, playercareerstats
from nba_api.stats.static import players
import pandas as pd
import time
import os

def get_player_id(player_name):
    """
    get the player id from the give player full name

    Parameters:
        player_name str: full name of player

    Returns:
        int: player id

    """
    player_dict = players.find_players_by_full_name(player_name)
    if player_dict != None:
        return player_dict[0]["id"]
    else:
        return None
    


def get_season_shot_data(player_id, season):
    """
    get the shot data for a specified player from a specific season using the nba api
    shot data is also filtered to only contain shots taken in the last 5 mins of games (clutch time)

    Parameters:
        player_id 
        int: id of player to search for from nba data
        season 
        str: the season of the shot data

    Returns:
        pd.DataFrame: a data frame containing all players shots in last 5 mins of games that season
    """
    time.sleep(1) #delay added to respect API rate limits
    print("shot data for season" + str(season))
    try:
        #feteches the relevant data of shots from NBA stats API
        season_shot_chart = shotchartdetail.ShotChartDetail(team_id=0,
                                                                player_id=player_id,
                                                                season_nullable=season,
                                                                season_type_all_star="Regular Season",
                                                                clutch_time_nullable= "Last 5 Minutes",
                                                                context_measure_simple="FGA")
        #remove unnessary columns
        season_shot_chart_df = season_shot_chart.get_data_frames()[0][['MINUTES_REMAINING',
                                                                        'EVENT_TYPE', 
                                                                        'ACTION_TYPE', 
                                                                        'SHOT_TYPE', 
                                                                        'SHOT_ZONE_BASIC', 
                                                                        'SHOT_ZONE_AREA', 
                                                                        'SHOT_ZONE_RANGE', 
                                                                        'SHOT_DISTANCE', 
                                                                        'LOC_X', 
                                                                        'LOC_Y',
                                                                        'SHOT_MADE_FLAG']]
        return season_shot_chart_df
    except Exception as e:
        print(f"unable to fetch data for season: {e}")
        #returns an empty dataframe with matchinh columns
        return pd.DataFrame(columns=['MINUTES_REMAINING',
                                    'EVENT_TYPE', 
                                    'ACTION_TYPE', 
                                    'SHOT_TYPE', 
                                    'SHOT_ZONE_BASIC', 
                                    'SHOT_ZONE_AREA', 
                                    'SHOT_ZONE_RANGE', 
                                    'SHOT_DISTANCE', 
                                    'LOC_X', 
                                    'LOC_Y',
                                    'SHOT_MADE_FLAG'])

def get_career_shot_data(player_id):
    time.sleep(1)
    print("fetching player career")
    career = playercareerstats.PlayerCareerStats(player_id= player_id)
    career_df = career.get_data_frames()[0]
    years = career_df["SEASON_ID"].unique()
    player_clutch_shot_data = pd.DataFrame()
    for year in years:
        season_shot_data = get_season_shot_data(player_id, year)
        if season_shot_data is not None:
            player_clutch_shot_data = pd.concat([player_clutch_shot_data,season_shot_data], ignore_index= True)
        
    return player_clutch_shot_data


def player_shots_csv(player_name):
    player_id = get_player_id(player_name)
    player_data = get_career_shot_data(player_id)
    player_name_formatted = player_name.replace(" ", "_")
    player_data.to_csv(f"../data/{player_name_formatted}_clutch.csv", index= False)


