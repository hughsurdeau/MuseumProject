import os
import pandas as pd
import numpy as np

path = os.getcwd()
top_dir = os.path.dirname(os.path.dirname(path))
par_dir = os.path.dirname(path)

wanderer_prism_file = par_dir + "/data/csv/prism_data.csv"
crowd_prism_file = par_dir + "/data/csv/crowd_size.csv"

wanderer_df = pd.read_csv(wanderer_prism_file)
crowd_df = pd.read_csv(crowd_prism_file)


room_map = {"lobby": "LobbyLeft",
            "left_gallery": "G1Left",
            "right_gallery": "G2Left"}


def get_wanderer_probability(w, s):
    wanderer_var = "Wanderer Prob (r=1)"
    val = wanderer_df.loc[(wanderer_df['W'] == w) & (wanderer_df['S'] ==s )][wanderer_var].values[0]
    return val


def binned_ratio(ratio):
    """
    Bins the input ratio into a preselected PRISM ratio
    :param ratio:
    :return:
    """
    if ratio < 2:
        return float(round(ratio * 10) / 10)
    elif ratio < 4:
        return float((round((ratio * 10)/2) * 2) / 10)
    else:
        return min(float(round(ratio)), 10)


def get_room_probability(room, ratio):
    ratio = binned_ratio(ratio)
    room = room_map[room]
    val = crowd_df.loc[(crowd_df['Crowd'] == ratio)][room].values[0]
    return val


def guassian_dist(mean, dev, min_val, max_val):
    num = np.random.normal(mean, dev)
    num = round(num)
    num = max(min_val, num)
    num = min(max_val, num)
    return num

