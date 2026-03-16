import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

def load_and_preprocess_data(dataset_path: str):
    """
    Loads dataset, applies StandardScaler to Amount,
    separates features and labels.
    """
    # Load dataset
    df = pd.read_csv(dataset_path)

    # Scale the Amount column
    scaler = StandardScaler()
    df['Amount'] = scaler.fit_transform(df['Amount'].values.reshape(-1, 1))

    # Drop Time as it might not be relevant enough for finding general anomalies (optional, but standard practice)
    df = df.drop(['Time'], axis=1)

    # Separate features and labels
    X = df.drop(['Class'], axis=1).values
    y = df['Class'].values
    
    return X, y, scaler

def get_normal_transactions_for_training(X, y):
    """
    Extracts only normal transactions (Class == 0) for training the autoencoder.
    """
    normal_indices = y == 0
    X_normal = X[normal_indices]
    
    return X_normal
