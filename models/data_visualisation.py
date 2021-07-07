import pandas as pd
import matplotlib.pyplot as plt

#Fonts
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = 'Helvetica'

#Axxes styles
plt.rcParams['axes.edgecolor']='#333F4B'
plt.rcParams['axes.linewidth']=0.8
plt.rcParams['xtick.color']='#333F4B'
plt.rcParams['ytick.color']='#333F4B'

class MuseumVisualisation:
    """
    Takes pandas dataframe and converts it into a gif
    for visualisation purposes

    Also includes live graphs and generic graph making etc
    """
    def __init__(self, df):
        self.df = df

    @staticmethod
    def graph_time_step(positions, wanderers):
        """
        The building has 3 rooms that need to be modelled and 10 artworks
        Rooms: lobby, gallery, gallery2, exit
        Art: 0-9

        Potential improvement - add also the ratio of wanderes to
        linear walkers
        :param positions:
        :return:
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        y = range(len(positions))
        ax.bar(y, positions)
        ax.bar(y, wanderers)
        ax.set_xlabel('Painting Number')
        ax.set_ylabel('Number of Viewers')
        ax.set_ylim(0, 100)
        fig.show()


    def animate_time_steps(self):
        pass

example = [2, 2, 1, 3, 0, 3, 2, 5, 3]
wands = [1, 1, 1, 0, 0, 3, 2, 1, 1]
MuseumVisualisation.graph_time_step(example, wands)
