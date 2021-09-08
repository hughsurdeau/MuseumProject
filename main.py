from models.museum_model import *


# Model Paramters
prism_integration = True
wanderer_threshold = 0.5
population_ratio = 20
day_length = 1000 # Length of day (in time steps)
number_of_days = 10 # Number of days to simulates


if __name__ == "__main__":

    parameters = {
        'population': population_ratio,
        'steps': day_length * number_of_days,
    }

    file_path = par_dir + "/data/csv/test.csv"
    model = MuseumModel(parameters)
    model.setup(prism_integration, wanderer_threshold, day_length, number_of_days)
    results = model.run()
    print(results.variables.MuseumModel)
    curr_time = str(datetime.datetime.now())
    results.variables.MuseumModel.to_csv(file_path)

