import { useState } from 'react'
import FraudForm from './components/FraudForm'
import './App.css'

function App() {
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  return (
    <div className="app-container">
      <header className="app-header animate-fade-in">
        <div className="logo">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="url(#primary-gradient)" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <defs>
              <linearGradient id="primary-gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stopColor="#6366f1" />
                <stop offset="100%" stopColor="#a855f7" />
              </linearGradient>
            </defs>
            <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
            <path d="M12 8v4"></path>
            <path d="M12 16h.01"></path>
          </svg>
        </div>
        <h1>Smart Fraud Detection System</h1>
        <p>AI-powered anomaly detection using Deep Autoencoders</p>
      </header>

      <main className="app-content animate-fade-in" style={{ animationDelay: '0.1s' }}>
        <FraudForm onResult={setResult} onError={setError} />

        {error && (
          <div className="result-card error glass-effect animate-fade-in">
            <div className="icon">⚠️</div>
            <div className="content">
              <h3>Error</h3>
              <p>{error}</p>
            </div>
          </div>
        )}

        {result && (
          <div className={`result-card glass-effect animate-fade-in ${result.prediction === 'Fraud' ? 'fraud' : 'normal'}`}>
            <div className="icon">
              {result.prediction === 'Fraud' ? '🚨' : '✅'}
            </div>
            <div className="content">
              <h3>{result.prediction === 'Fraud' ? 'Fraudulent Transaction Detected!' : 'Transaction Normal'}</h3>
              <div className="stats">
                <div className="stat-box">
                  <span className="label">Prediction</span>
                  <span className="value">{result.prediction}</span>
                </div>
                <div className="stat-box">
                  <span className="label">Reconstruction Error</span>
                  <span className="value error-val">{result.reconstruction_error.toFixed(4)}</span>
                </div>
                <div className="stat-box">
                  <span className="label">Threshold</span>
                  <span className="value">{result.threshold_used.toFixed(4)}</span>
                </div>
              </div>
            </div>
          </div>
        )}
      </main>
      
      <footer className="app-footer animate-fade-in" style={{ animationDelay: '0.2s' }}>
        <p>Powered by FastAPI & Vite + React</p>
      </footer>
    </div>
  )
}

export default App
