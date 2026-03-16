from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tensorflow as tf
import numpy as np
import os
import joblib
from src.anomaly_detection import calculate_reconstruction_error, classify_anomaly

# Trigger reload
app = FastAPI(title="Smart Fraud Detection API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TransactionData(BaseModel):
    features: list[float]

# Model and configs
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'autoencoder_model.h5')
THRESHOLD_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'threshold.txt')
SCALER_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'scaler.pkl')

model = None
scaler = None
THRESHOLD = 5.0 # default fallback

@app.on_event("startup")
def load_artifacts():
    global model, THRESHOLD, scaler
    try:
        if os.path.exists(MODEL_PATH):
            model = tf.keras.models.load_model(MODEL_PATH)
            print("Model loaded successfully.")
        else:
            print(f"Warning: Model not found at {MODEL_PATH}. Prediction will fail.")
            
        if os.path.exists(THRESHOLD_PATH):
            with open(THRESHOLD_PATH, 'r') as f:
                THRESHOLD = float(f.read().strip())
                print(f"Threshold loaded: {THRESHOLD}")
                
        if os.path.exists(SCALER_PATH):
            scaler = joblib.load(SCALER_PATH)
            print("Scaler loaded successfully.")
    except Exception as e:
        print(f"Error loading model/artifacts: {e}")

@app.get("/")
def root():
    return {"message": "Fraud Detection API Running"}

@app.post("/predict")
def predict_fraud(transaction: TransactionData):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded. Train the model first.")
        
    try:
        # Convert input to numpy array and shape properly (batch_size, num_features)
        input_data = np.array(transaction.features).reshape(1, -1)
        
        # Scale the amount feature if we have the scaler (Amount is the 29th feature, index 28)
        if scaler and input_data.shape[1] == 29:
            input_data[0, 28] = scaler.transform([[input_data[0, 28]]])[0][0]
        
        # Pass through autoencoder model
        reconstructed_data = model.predict(input_data)
        
        # Calculate reconstruction error
        error = calculate_reconstruction_error(input_data, reconstructed_data)[0]
        
        # Compare with threshold
        prediction = classify_anomaly(error, THRESHOLD)
        
        return {
            "prediction": prediction,
            "reconstruction_error": float(error),
            "threshold_used": float(THRESHOLD)
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
