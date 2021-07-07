import pandas as pd
import matplotlib.pyplot as plt

class MuseumVisualisation:
    """
    Takes pandas dataframe and converts it into a gif
    for visualisation purposes
    """
    def __init__(self, df):
        self.df = df

    