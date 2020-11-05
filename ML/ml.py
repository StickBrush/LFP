from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
import pickle
import json

def train_model(model, X: list, y: list, out_filename: str):
    model.fit(X, y)
    with open(out_filename, 'wb') as out_model:
        pickle.dump(model, out_model)

def train_linear(X: list, y: list, out_filename: str):
    model = LinearRegression()
    train_model(model, X, y, out_filename)

def train_svm(X: list, y: list, out_filename: str):
    model = SVR()
    train_model(model, X, y, out_filename)

def train_neural(X: list, y: list, out_filename: str):
    model = MLPRegressor()
    train_model(model, X, y, out_filename)

def train_all_from_files(in_files: list):
    for file in files:
        out_file = file[:-5]
        with open(file, 'r') as in_json:
            data = json.load(in_json)
        X = data['ml_x']
        y = data['ml_y']
        train_linear(X, y, out_file+"Linear.lfp")
        train_neural(X, y, out_file+"Neural.lfp")
        train_svm(X, y, out_file+"SVM.lfp")

if __name__ == "__main__":
    files = ["ML_COMB_1+2+3.json", "ML_COMB_1+2+4.json", "ML_COMB_1+3+4.json", "ML_COMB_2+3+4.json"]
    train_all_from_files(files)