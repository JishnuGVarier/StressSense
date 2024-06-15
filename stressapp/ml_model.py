# ml_model.py

import joblib

def load_model(file_path):
    # Load the model from the specified file path
    model,scaler = joblib.load(file_path)
    return model,scaler

def predict(input_data):
    model,scaler = load_model('model_and_scaler.pkl')
    X_scaled = scaler.transform(input_data)
    prediction = model.predict(X_scaled)
    return prediction

