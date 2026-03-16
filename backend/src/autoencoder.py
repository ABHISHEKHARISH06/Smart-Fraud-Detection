import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Dropout

def build_autoencoder(input_dim: int) -> Model:
    """
    Builds an Autoencoder neural network.
    Encoder compresses feature vectors, Decoder reconstructs them.
    """
    # Encoder
    input_layer = Input(shape=(input_dim,))
    encoder = Dense(16, activation="relu")(input_layer)
    encoder = Dropout(0.2)(encoder)
    encoder = Dense(8, activation="relu")(encoder)
    
    # Decoder
    decoder = Dense(8, activation="relu")(encoder)
    decoder = Dropout(0.2)(decoder)
    decoder = Dense(16, activation="relu")(decoder)
    decoder = Dense(input_dim, activation="linear")(decoder)

    # Autoencoder Model
    autoencoder = Model(inputs=input_layer, outputs=decoder)
    
    # Compile with MSE loss
    autoencoder.compile(optimizer='adam', loss='mean_squared_error')
    
    return autoencoder
