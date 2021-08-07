"""
Main TODO:
    1 - Add time piping into main sim - DONE
    2 - Make new nonlinear museum layout -DONE?
    3 - Test to make sure everything is working ok - DONE
    3.5 - Make sure there are different versions for PRISM and not PRISM
    4 - Add in PRISM data for wandering vs linear -
    5 - Make more complex PRISM model for wandering vs linear - Sunday
    5.5 - Automated PRISM shit
    6 - Make PRISM model for # of people up ahead - Monday
    7 - Integrate data - Tuesday
    8 - Write etc

TODO: Maybe interesting approaches
    1 - Maybe a volume level of each room?
"""
from models.museum_model import *

if __name__ == "__main__":

    parameters = {
        'population': 20,
        'steps': 1000,
    }

    model = MuseumModel(parameters)
    results = model.run()
    print(results.variables.MuseumModel)
    curr_time = str(datetime.datetime.now())
    file_path = "/Users/hughsurdeau/PycharmProjects/MuseumProject/data/csv/linear_museum_45AT.csv"
    results.variables.MuseumModel.to_csv(file_path)

