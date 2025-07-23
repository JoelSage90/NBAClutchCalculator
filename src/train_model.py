from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib

league_shots = pd.read_csv("../data/all_shots_2024-25.csv")
features = ["MINUTES_REMAINING",
            "ACTION_TYPE",
            "SHOT_TYPE", 
            "SHOT_ZONE_BASIC",
            "SHOT_ZONE_AREA",
            "SHOT_ZONE_RANGE",
            "SHOT_DISTANCE",
            "LOC_X",
            "LOC_Y"]
target = "SHOT_MADE_FLAG"

x = pd.get_dummies(league_shots[features],drop_first=True) #one-hot encoding for the features
joblib.dump(x.columns, "../models/logistic_regression_shot_model_columns.joblib")
y = league_shots[target]
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2, random_state=67)

model = LogisticRegression(solver="liblinear",max_iter=1000)
model.fit(x_train,y_train)
joblib.dump(model, "../models/logistic_regression_shot_model.joblib")

y_pred = model.predict_proba(x_test)[:,0]
y_prob = model.predict_proba(x_test)[:,1]
model_eval_df = x_test.copy()
model_eval_df["prediction"] = y_pred
model_eval_df["expected prob"] = y_prob
model_eval_df["actual"] = y_test
model_eval_df.to_csv("../data/model_eval.csv", index= False)
