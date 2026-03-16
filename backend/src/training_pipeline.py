import os
import numpy as np
from src.preprocessing import load_and_preprocess_data, get_normal_transactions_for_training
from src.autoencoder import build_autoencoder
from src.anomaly_detection import calculate_reconstruction_error
from sklearn.model_selection import train_test_split

# Config
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'creditcard.csv')
MODEL_SAVE_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'autoencoder_model.h5')

def run_pipeline():
    print("1. Loading and preprocessing dataset...")
    X, y, scaler = load_and_preprocess_data(DATA_PATH)
    
    # We only train on normal data
    X_normal = get_normal_transactions_for_training(X, y)
    
    # Split into train and validation sets (only normal data)
    X_train, X_val = train_test_split(X_normal, test_size=0.2, random_state=42)

    print(f"Training on {X_train.shape[0]} normal transactions.")
    
    input_dim = X_train.shape[1]
    
    print("2. Building Autoencoder...")
    autoencoder = build_autoencoder(input_dim)
    
    print("3. Training Autoencoder...")
    history = autoencoder.fit(
        X_train, X_train,
        epochs=15,
        batch_size=256,
        validation_data=(X_val, X_val),
        shuffle=True,
        verbose=1
    )
    
    print("4. Calculating reconstruction error threshold...")
    # Predict on validation normal data to find a good threshold
    reconstructions = autoencoder.predict(X_val)
    val_mse = calculate_reconstruction_error(X_val, reconstructions)
    
    # Set threshold as e.g. 99th percentile of validation reconstruction error
    threshold = np.percentile(val_mse, 99)
    print(f"Suggested threshold based on 99th percentile of normal data: {threshold}")

    print("5. Saving the model & scaler...")
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    autoencoder.save(MODEL_SAVE_PATH)
    
    import joblib
    scaler_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'scaler.pkl')
    joblib.dump(scaler, scaler_path)
    
    # Also save the suggested threshold somewhere if desired, e.g. as a text file
    threshold_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'threshold.txt')
    with open(threshold_path, 'w') as f:
        f.write(str(threshold))
        
    print(f"Model saved to {MODEL_SAVE_PATH}")
    print(f"Scaler saved to {scaler_path}")
    print(f"Threshold saved to {threshold_path}")

if __name__ == "__main__":
    if not os.path.exists(DATA_PATH):
        print(f"Error: Dataset not found at {DATA_PATH}. Please place creditcard.csv in backend/data/raw/.")
    else:
        run_pipeline()
