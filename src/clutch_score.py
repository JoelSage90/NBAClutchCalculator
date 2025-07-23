import joblib
from pathlib import Path
import pandas as pd


base_dir = Path(__file__).resolve().parent.parent
model_path = base_dir / "models" / "logistic_regression_shot_model.joblib"
columns_path = base_dir / "models" / "logistic_regression_shot_model_columns.joblib"
model = joblib.load(model_path)
model_columns = joblib.load(columns_path)


def clutch_multipler(min_left):
    """
    takes in the mins left to decide multipler for shot
    Parameters:
        min_left: number of mins left in the game
    """
    if min_left > 5:
        mutliplier = 1
    else:
        mutliplier = 1+ ((5-min_left) * 0.1)
    return mutliplier

def clutch_points(df):
    """
    calculates the clutch points per shot
    clutch points = base points *((1-model prob) * clutch time multipler)

    Parameters:
        df: players clutch shots
    """
    features = ["MINUTES_REMAINING",
            "ACTION_TYPE",
            "SHOT_TYPE", 
            "SHOT_ZONE_BASIC",
            "SHOT_ZONE_AREA",
            "SHOT_ZONE_RANGE",
            "SHOT_DISTANCE",
            "LOC_X",
            "LOC_Y"]
    x = pd.get_dummies(df[features],drop_first=True)
    x = x.reindex(columns=model_columns, fill_value=0)
    x = x.fillna(0)
    y = model.predict_proba(x)[:,1]
    
    df["model_prob"] = y
    df["BASE_POINTS"] = df['SHOT_TYPE'].apply(lambda x: 3 if x == "3PT Field Goal" else 2)
    df["CLUTCH_MULTI"] = df["MINUTES_REMAINING"].apply(clutch_multipler)
    df["CLUTCH_POINTS"] = df["BASE_POINTS"] * ((1-df["model_prob"])* df["CLUTCH_MULTI"])
    return df
         
def clutchness_calculator(df):
    """
    uses the clutch points generated from model and formula to calculate overall clutchness
    Parameters:
        df: players clutch shots
    """
    clutch_df = clutch_points(df)
    potential_clutch_points = clutch_df["CLUTCH_POINTS"].sum()
    actual_clutch_points = clutch_df[clutch_df["SHOT_MADE_FLAG"] ==1]["CLUTCH_POINTS"].sum()
    clutchness = (actual_clutch_points/potential_clutch_points) *200
    if clutchness > 100: #cap the clutch rating at 100
        clutchness = 100
    return clutchness



