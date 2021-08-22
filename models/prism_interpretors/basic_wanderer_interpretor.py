import os
import pandas as pd

path = os.getcwd()
top_dir = os.path.dirname(os.path.dirname(path))
par_dir = os.path.dirname(path)

wanderer_prism_file = par_dir + "/data/csv/prism_data.csv"
crowd_prism_file = par_dir + "/data/csv/crowd_size.csv"

wanderer_df = pd.read_csv(wanderer_prism_file)
crowd_df = pd.read_csv(crowd_prism_file)


def get_wanderer_probability(w, s):
    wanderer_var = "Wanderer Prob (r=1)"
    val = wanderer_df.loc[(wanderer_df['W'] == w) & (wanderer_df['S'] ==s )][wanderer_var].values[0]
    return val


def get_room_probability(room, ratio):
    val = crowd_df.loc(crowd_df['Crowd'] == ratio)[room].values[0]
    return val