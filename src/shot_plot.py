import matplotlib.pyplot as plt 
from matplotlib.patches import Polygon
import matplotlib.cm as cm
import matplotlib.colors as colors
from mplbasketball import Court
import pandas as pd
import numpy as np

def draw_half_court():
    court_nba = Court(court_type="nba", units="ft", origin="center")
    fig, ax = plt.subplots(figsize=(10, 7))
    court_nba.draw(ax=ax)
    ax.set_xlim(left= -47,right=-1)
    ax.set_ylim(bottom=-25,top=25)

    return fig,ax

def draw_sections(r_inner,r_outer,t1,t2,colour,fgp):
    n_points = 100
    theta1 = np.radians(t1)
    theta2 = np.radians(t2)
    #outer radius
    theta_outer = np.linspace(theta1, theta2, n_points)
    x_outer = -41.75 + r_outer * np.cos(theta_outer)
    y_outer = 0 + r_outer * np.sin(theta_outer)

    #inner radius
    theta_inner = np.linspace(theta2, theta1, n_points)
    x_inner = -41.75 + r_inner * np.cos(theta_inner)
    y_inner = 0 + r_inner * np.sin(theta_inner)


    xs = np.concatenate([x_outer, x_inner])
    ys = np.concatenate([y_outer, y_inner])
    polygon_points = np.column_stack([xs, ys])

    poly = Polygon(polygon_points, closed=True, color=colour, alpha=fgp)
    return poly

def draw_corner_sections(r,t1,t2,x_left,x_right,y_cap,colour,fgp):
    theta1 = np.radians(t1)
    theta2 = np.radians(t2)
    #arc
    theta_outer = np.linspace(theta1, theta2, 100)
    x_arc = -41.75 + r * np.cos(theta_outer)
    y_arc = 0 + r * np.sin(theta_outer)
    #using the edges of the arc points
    x_right_top = x_arc[-1]
    x_left_top = x_arc[0]
    y_right_top = y_arc[-1]
    y_left_top = y_arc[0]
    xs = np.concatenate([x_arc,[x_right_top,x_right,x_left,x_left_top]])
    ys = np.concatenate([y_arc,[y_right_top,y_cap,y_cap,y_left_top]])
    polygon_points = np.column_stack([xs, ys])

    poly = Polygon(polygon_points, closed=True, color=colour, alpha=fgp)
    return poly
theta4 = 68.31093183
theta3 = 22.7552756
theta5 = 45.53310372
def shot_section(r, theta):
    if r <= 8:
        return "layup"
    elif r >8 and r <=17:
        if theta <180 and theta >= theta5:
            return "right close midrange"
        elif theta <theta5 and theta >= -theta5:
            return "centre close midrange"
        elif theta <-theta5 and theta >= -180:
            return "left close midrange"
    elif r>17 and r <=23:
        if theta <180 and theta >= theta4:
            return "right corner midrange"
        elif theta <theta4 and theta >= theta3:
            return "right wing midrange"
        elif theta < theta3 and theta >= -theta3:
            return "centre midrange"
        elif theta < -theta3 and theta >= -theta4:
            return "left wing midrange"
        elif theta < -theta4 and theta >=-180:
            return "left corner midrange"
    elif r>23 and r<=30:
        if theta <180 and theta >= theta4:
            return "right corner three"
        elif theta <theta4 and theta >= theta3:
            return "right wing three"
        elif theta < theta3 and theta >= -theta3:
            return "centre three"
        elif theta < -theta3 and theta >= -theta4:
            return "left wing three"
        elif theta < -theta4 and theta >=-180:
            return "left corner three"
    elif r>30:
        return "deep three"
    else:
        return "out of range"


def draw_heat_map(player_df):
    fig,ax = draw_half_court()
    #adjust coords to match mplbasketball coords system
    player_df["LOC_X_ft"] = player_df["LOC_X"]/10
    player_df["LOC_Y_ft"] = player_df["LOC_Y"]/10
    player_df["LOC_X_ADJUSTED"] = player_df["LOC_Y_ft"] - 41.75
    player_df["LOC_Y_ADJUSTED"] = player_df["LOC_X_ft"]
    #polar coords
    player_df["RADIUS"] = np.sqrt((player_df["LOC_X_ADJUSTED"]+41.75)**2 + player_df["LOC_Y_ADJUSTED"]**2)
    player_df["THETA"] = np.degrees(np.arctan2(player_df["LOC_Y_ADJUSTED"],player_df["LOC_X_ADJUSTED"]+41.75))
    player_df["SHOT_SECTION"] = player_df.apply(lambda row: shot_section(row["RADIUS"], row["THETA"]), axis=1)

    sections = player_df["SHOT_SECTION"].unique()
    section_percentages = {} #stores percentages for each section in dict

    for section in sections:
        section_value_list = []
        try:
            section_percent = len(player_df[(player_df["SHOT_SECTION"] == section) & (player_df["SHOT_MADE_FLAG"] ==1)])/len(player_df[player_df["SHOT_SECTION"] == section])
            section_percent = np.round(section_percent,4)
        except ZeroDivisionError:
            print(f"no shots in this section {section}")
            section_percent = 0
        finally:
            section_value_list.append(section_percent)
            section_value_list.append(len(player_df[(player_df["SHOT_SECTION"] == section) & (player_df["SHOT_MADE_FLAG"] ==1)])) #number of made shots
            section_value_list.append(len(player_df[player_df["SHOT_SECTION"] == section])) #number of taken shots
            #[percentage,madeshots,taken shots]
            section_percentages[section] = section_value_list

    def label_section(r1,r2,t1,t2,section,t3):
        r_mid = (r1+r2)/2
        t_mid = np.radians((t1+t2)/2)
        #convert from polar to x and y
        x =r_mid * np.cos(t_mid) -41.75
        y =r_mid * np.sin(t_mid)
        ax.text(x,y,f"{section_percentages[section][1]}/{section_percentages[section][2]}", ha="center", va="center",rotation= t3)
