# Backend for Smart Fraud Detection System

This directory contains the machine learning pipeline and FastAPI server for fraud detection.

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Creating the Model
1. Ensure the Kaggle credit card fraud dataset (`creditcard.csv`) is placed at `backend/data/raw/creditcard.csv`.
2. Run the training pipeline from the `backend/` directory:
   ```bash
   python -m src.training_pipeline
   ```
   This will output an `autoencoder_model.h5` and a `threshold.txt` in the `models/` directory.

## Running the API Server

Start the FastAPI backend with:

```bash
uvicorn api.main:app --reload
```

The server will start at `http://localhost:8000`.

- Test endpoint: `GET http://localhost:8000/`
- Prediction endpoint: `POST http://localhost:8000/predict`
- Interactive Docs: `http://localhost:8000/docs`
