import numpy as np

def calculate_reconstruction_error(original_features, reconstructed_features):
    """
    Calculates the Mean Squared Error (MSE) between original and reconstructed features.
    """
    mse = np.mean(np.power(original_features - reconstructed_features, 2), axis=1)
    return mse

def classify_anomaly(error_score, threshold):
    """
    Classifies a transaction as an anomaly (fraud) if the error exceeds the threshold.
    """
    is_anomaly = error_score > threshold
    return "Fraud" if is_anomaly else "Normal"
