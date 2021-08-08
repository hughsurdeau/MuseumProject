import os
import pandas as pd

path = os.getcwd()
top_dir = os.path.dirname(os.path.dirname(path))

prism_file = top_dir + "/data/csv/prism_data.csv"


df = pd.read_csv(prism_file)


def get_wanderer_probability(w, s):
    wanderer_var = "Wanderer Prob (r=1)"
    val = df.loc[(df['W'] == w) & (df['S'] ==s )][wanderer_var].values[0]
    return val
