import { useState } from 'react';
import { predictFraud } from '../services/api';
import './FraudForm.css';

export default function FraudForm({ onResult, onError }) {
  const [inputType, setInputType] = useState('manual'); // 'manual' | 'normal' | 'fraud' | 'random'
  const [manualData, setManualData] = useState('');
  const [randomData, setRandomData] = useState('');
  const [loading, setLoading] = useState(false);

  // Exact 29 features: V1-V28, and Amount (Time is dropped during training)
  const sampleNormal = "-1.359807, -0.072781, 2.536347, 1.378155, -0.338321, 0.462388, 0.239599, 0.098698, 0.363787, 0.090794, -0.551600, -0.617801, -0.991390, -0.311169, 1.468177, -0.470401, 0.207971, 0.025791, 0.403993, 0.251412, -0.018307, 0.277838, -0.110474, 0.066928, 0.128539, -0.189115, 0.133558, -0.021053, 149.62";

  const sampleFraud = "-2.312227, 1.951992, -1.609851, 3.997906, -0.522188, -1.426545, -2.537387, 1.391657, -2.770089, -2.772272, 3.202033, -2.899907, -0.595222, -4.289254, 0.389724, -1.140747, -2.830056, -0.016822, 0.416956, 0.126911, 0.517232, -0.035049, -0.465211, 0.320198, 0.044519, 0.177840, 0.261145, -0.143276, 0.00";

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    onResult(null);
    onError(null);

    let dataToProcess = manualData;
    if (inputType === 'normal') dataToProcess = sampleNormal;
    if (inputType === 'fraud') dataToProcess = sampleFraud;
    if (inputType === 'random') dataToProcess = randomData;

    try {
      const features = dataToProcess.split(',').map(val => parseFloat(val.trim()));
      
      if (features.some(isNaN) || features.length !== 29) {
        throw new Error(`Please provide exactly 29 valid CSV numbers. You provided ${features.length}.`);
      }

      const result = await predictFraud(features);
      onResult({ ...result, features });
    } catch (err) {
       onError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="card form-container glass-effect">
      <h2>Analyze Transaction</h2>
      <p className="subtitle">Choose a sample standard transaction or provide exact PCA features.</p>
      
      <div className="tab-buttons">
        <button 
          type="button"
          className={`tab-btn ${inputType === 'normal' ? 'active' : ''}`}
          onClick={() => setInputType('normal')}
        >
          ✅ Safe Example
        </button>
        <button 
          type="button"
          className={`tab-btn ${inputType === 'fraud' ? 'active danger' : ''}`}
          onClick={() => setInputType('fraud')}
        >
          🚨 Fake Example
        </button>
        <button 
          type="button"
          className={`tab-btn ${inputType === 'manual' ? 'active' : ''}`}
          onClick={() => setInputType('manual')}
        >
          📝 Manual Input
        </button>
        <button 
          type="button"
          className={`tab-btn ${inputType === 'random' ? 'active' : ''}`}
          onClick={() => {
            setInputType('random');
            if (!randomData) setRandomData(Array.from({ length: 29 }, () => (Math.random() * 10 - 5).toFixed(6)).join(', '));
          }}
        >
          🎲 Random Input
        </button>
      </div>

      <form onSubmit={handleSubmit}>
        {inputType === 'manual' || inputType === 'random' ? (
          <div className="input-group">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
              <label htmlFor="features">Transaction Features (V1-V28, and Amount)</label>
              {inputType === 'random' && (
                <button 
                  type="button" 
                  className="small-btn" 
                  onClick={() => setRandomData(Array.from({ length: 29 }, () => (Math.random() * 10 - 5).toFixed(6)).join(', '))}
                >
                  🔄 Regenerate
                </button>
              )}
            </div>
            <textarea 
              id="features"
              className="feature-input"
              value={inputType === 'manual' ? manualData : randomData}
              onChange={(e) => inputType === 'manual' ? setManualData(e.target.value) : setRandomData(e.target.value)}
              placeholder="e.g. -1.3598, -0.0727... (29 values total)"
              rows={5}
              required
            />
          </div>
        ) : (
          <div className="sample-display">
             <div className="icon">{inputType === 'normal' ? '✅' : '🚨'}</div>
             <p>{inputType === 'normal' ? 'Normal Data selected for testing.' : 'Fake (Fraudulent) Data selected.'}</p>
             <span className="small-text">(29 features perfectly matched to the model logic)</span>
          </div>
        )}

        <button 
          type="submit" 
          className={`btn-primary ${inputType === 'fraud' ? 'fraud-btn' : ''}`} 
          disabled={loading || (inputType === 'manual' && !manualData) || (inputType === 'random' && !randomData)}
        >
          {loading ? (
             <span className="spinner"></span>
          ) : (
            "Run Deep Autoencoder"
          )}
        </button>
      </form>
    </div>
  );
}
