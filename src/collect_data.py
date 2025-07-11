from nba_api.stats.endpoints import shotchartdetail, playercareerstats, commonteamroster
from nba_api.stats.static import players, teams
import pandas as pd
import time


def get_player_id(player_name):
    """
    get the player id from the give player full name

    Parameters:
        player_name: full name of player

    Returns:
        int: player id

    """
    player_dict = players.find_players_by_full_name(player_name)
    if player_dict != None:
        return player_dict[0]["id"]
    return None
    

def get_season_nonclutch_shot_data(player_id, season):
    """
    get the shot data for a specified player from a specific season using the nba api

    Parameters:
        player_id: int, id of player to search for from nba data
        season: str, the season of the shot data

    Returns:
        pd.DataFrame: a data frame containing all players shots in that season
    """
    time.sleep(1) #delay added to respect API rate limits
    print("shot data for season" + str(season))
    try:
        #feteches the relevant data of shots from NBA stats API
        season_shot_chart = shotchartdetail.ShotChartDetail(team_id=0,
                                                                player_id=player_id,
                                                                season_nullable=season,
                                                                season_type_all_star="Regular Season",
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


def get_season_shot_data(player_id, season):
    """
    get the shot data for a specified player from a specific season using the nba api
    shot data is also filtered to only contain shots taken in the last 5 mins of games (clutch time)

    Parameters:
        player_id: int, id of player to search for from nba data
        season: str, the season of the shot data

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
    """
    this function is used to get all the clutch shots in the players career rather than just one season

    Parameters:
        player_id: int, id of the player to get shots for

    Returns:
        pd.DataFrame: data frame containing players career clutch shots
    """
    time.sleep(0.5)
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
    """
    Creates a CSV files for the career clutch shots
    Parameters:
        player_name: str, name of the player to create csv for
    """
    player_id = get_player_id(player_name)
    player_data = get_career_shot_data(player_id)
    player_name_formatted = player_name.replace(" ", "_")
    player_data.to_csv(f"../data/{player_name_formatted}_clutch.csv", index= False)


def all_players():
    """
    retrives all players from the nba api for the 2024-25 season
    Returns:
        pd.DataFrame: data frame of all players in NBA with names and ids
    """
    teams_list = teams.get_teams()
    all_players = []
    for team in teams_list:
        
        team_id = team['id']
        print(f"getting data for team {team_id}")
        roster = commonteamroster.CommonTeamRoster(team_id=team_id, season='2024-25')
        time.sleep(0.5)
        players_list = roster.get_data_frames()[0]
        all_players.append(players_list)
    all_players_df = pd.concat(all_players, ignore_index= True)
    all_players_df_filtered = all_players_df[['PLAYER','PLAYER_ID']]
    return all_players_df_filtered


def league_shot_chart():
    """
    Creates a csv file containing all the shots taken by all players in the 2024-25 season
    """
    players = all_players()
    header_write = True
    for _,row in players.iterrows():
        try:
            player_id = row['PLAYER_ID']
            player_shot_chart = get_season_nonclutch_shot_data(player_id,'2024-25')
            player_shot_chart_filtered = player_shot_chart[['MINUTES_REMAINING',
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
            #append to csv file on each iteration
            player_shot_chart_filtered.to_csv("../data/all_shots_2024-25.csv", index= False, mode= "a", header=header_write)
            header_write = False
        except Exception as e:
            print(f"unable to get shots for player:{player_id}")
            continue
