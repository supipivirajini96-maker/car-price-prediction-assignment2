import numpy as np
import pickle
import cloudpickle

import os
import pickle

### for old model

# Load trained model and scaler
model_path = os.path.join(os.path.dirname(__file__), "../models/car-prediction.model")
model = pickle.load(open(model_path, "rb"))

scaler_path = os.path.join(os.path.dirname(__file__), "../models/scaler.pkl")
scaler = pickle.load(open(scaler_path, "rb"))

# Load defaults for missing values
default_path = os.path.join(os.path.dirname(__file__), "../models/defaults.pkl")
defaults = pickle.load(open(default_path, "rb"))

def predict_car_price(sample: np.ndarray) -> float:
    

    # Predict the car price
    predicted_price = model.predict(sample)

    # Undo log transform 
    predicted_price = np.exp(predicted_price)

    return float(predicted_price[0])



def fill_missing_values(transmission, max_power):
    # Handle missing categorical values of transmission
    if transmission is None:
        probs = defaults["transmission_ratio"]
        transmission = np.random.choice(list(probs.keys()), p=list(probs.values()))

    # Handle missing numeric values of max_power
    if max_power is None:
        max_power = defaults["mean_max_power"]  

    return transmission, max_power



### for new model
import mlflow.pyfunc

# Path can be local run artifacts or registered model URI
model_uri = "../code/models/artifacts/"  # local folder with MLmodel, or "runs:/<run_id>/car_model"

model_new = mlflow.pyfunc.load_model(model_uri)


def predict_car_price_new(sample: np.ndarray) -> float:
    


    # Predict the car price
    predicted_price = model_new.predict(sample)

    # Undo log transform 
    predicted_price = np.exp(predicted_price)

    return float(predicted_price[0])












# Example
#if __name__ == "__main__":
    # Replace with actual user input
    #sample = np.array([[1, 67.05, 998.00, 2009.00]])  # example
    #print("Predicted Car Price:", predict_car_price(sample))
