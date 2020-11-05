import pickle
import json
import os
import numpy as np
from sklearn.metrics import f1_score, precision_score, recall_score, accuracy_score
from tqdm import tqdm

DELTAS = {
    '1': {
        '0': 96,
        '1': 144,
        '2': 192,
        '3': 240,
        '4': 288
    },
    '2': {
        '0': 960,
        '1': 1440,
        '2': 1920,
        '3': 2400,
        '4': 2880
    },
    '3': {
        '0': 480,
        '1': 720,
        '2': 960,
        '3': 1200,
        '4': 1440
    },
    '4': {
        '0': 288,
        '1': 576,
        '2': 864,
        '3': 1152,
        '4': 1440
    }
}

""" DELTAS = {
    '0': 960,
    '1': 1440,
    '2': 1920,
    '3': 2400,
    '4': 2880
} """

ML_MODEL = {
    1: '2+3+4',
    2: '1+3+4',
    3: '1+2+4',
    4: '1+2+3'
}

if __name__ == "__main__":
    for model in [1, 2, 3, 4]:
        boolean_data = {'linear': {'f1': [], 'precision': [], 'recall': [], 'accuracy': [
        ]}, 'neural': {'f1': [], 'precision': [], 'recall': [], 'accuracy': []}}
        predicted_data = {'actual': [], 'linear': [], 'neural': []}
        TEST_DIR = 'GR_{}_TEST'.format(model)
        files = list(map(lambda x: os.path.join(TEST_DIR, x), os.listdir(TEST_DIR)))
        for file in tqdm(files):
            funct = file[-6]
            delta_t = DELTAS[str(model)][funct]
            with open(file, 'r') as in_json:
                test_data = json.load(in_json)
            linear_model = 'ML_COMB_'+ML_MODEL[model]+'Linear.lfp'
            neural_model = 'ML_COMB_'+ML_MODEL[model]+'Neural.lfp'
            svm_model = 'ML_COMB_'+ML_MODEL[model]+'SVM.lfp'
            with open(linear_model, 'rb') as in_l_model:
                linear_pred = pickle.load(in_l_model)
            with open(neural_model, 'rb') as in_nn_model:
                neural_pred = pickle.load(in_nn_model)
            with open(svm_model, 'rb') as in_svm_model:
                svm_pred = pickle.load(in_svm_model)
            for x_test, actual_lt in zip(test_data['ml_x'], test_data['ml_y']):
                time_since_fail = delta_t - actual_lt
                predicted_data['actual'].append((time_since_fail, actual_lt))
                pred_linear = linear_pred.predict(np.array(x_test).reshape((1, -1)))[0]
                predicted_data['linear'].append((time_since_fail, pred_linear))
                pred_neural = neural_pred.predict(np.array(x_test).reshape((1, -1)))[0]
                predicted_data['neural'].append((time_since_fail, pred_neural))
                pred_svm = svm_pred.predict(np.array(x_test).reshape((1, -1)))[0]
                predicted_data['svm'].append((time_since_fail, pred_svm))
        with open('SensitivityG{}.json'.format(model), 'w') as out_json:
            json.dump(predicted_data, out_json)

