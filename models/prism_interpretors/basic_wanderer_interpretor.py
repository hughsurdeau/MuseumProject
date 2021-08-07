import os
import pandas as pd

path = os.getcwd()
top_dir = os.path.dirname(os.path.dirname(path))

prism_file = top_dir + "/data/csv/prism_data.csv"


db = pd.read_csv(prism_file)

print(db)

class BasicWandererAPI:

    def __init__(self):
        pass