from models.museum_model import *

if __name__ == "__main__":

    parameters = {
        'population': 20,
        'steps': day_length * number_of_days,
    }

    file_path = par_dir + "/data/csv/test.csv"
    model = MuseumModel(parameters)
    results = model.run()
    print(results.variables.MuseumModel)
    curr_time = str(datetime.datetime.now())
    results.variables.MuseumModel.to_csv(file_path)

