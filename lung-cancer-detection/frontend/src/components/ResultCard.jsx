import React from 'react';
import './ResultCard.css';

const ResultCard = ({ predictionData, imageUrl, onReset }) => {
  if (!predictionData) return null;

  const { prediction, confidence_score, filename } = predictionData;
  
  // Format the confidence score to a clean percentage (e.g., 0.985 -> 98.5%)
  const confidencePercent = (confidence_score * 100).toFixed(1);
  
  // Determine if result is Malignant or Normal to apply color styling dynamically
  const isMalignant = prediction.toLowerCase() === 'malignant';
  
  return (
    <div className="result-container">
      <div className="result-header">
        <h2>Analysis Complete</h2>
        <span className={`status-badge ${isMalignant ? 'badge-danger' : 'badge-success'}`}>
          {isMalignant ? 'Attention Needed' : 'Normal'}
        </span>
      </div>

      <div className="result-body">
        <div className="scan-preview-wrapper">
          <img src={imageUrl} alt="Analyzed CT Scan" className="analyzed-scan" />
        </div>
        
        <div className="analysis-details">
          <div className="detail-row">
            <span className="detail-label">File Analyzed</span>
            <span className="detail-value text-muted">{filename}</span>
          </div>
          
          <div className="detail-row">
            <span className="detail-label">Model Prediction</span>
            <span className={`prediction-text ${isMalignant ? 'text-danger' : 'text-success'}`}>
              {prediction}
            </span>
          </div>

          <div className="confidence-section">
            <div className="confidence-header">
              <span className="detail-label">AI Confidence Score</span>
              <span className="confidence-value">{confidencePercent}%</span>
            </div>
            
            {/* Creates a dynamic progress bar filling up to the percentage */}
            <div className="progress-bar-bg">
              <div 
                className={`progress-bar-fill ${isMalignant ? 'fill-danger' : 'fill-success'}`}
                style={{ width: `${confidencePercent}%` }}
              ></div>
            </div>
          </div>
          
          {isMalignant && (
            <div className="warning-callout">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="warning-icon">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line x1="12" y1="9" x2="12" y2="13"></line>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
              </svg>
              <p>Malignant tissues detected. Immediate medical review and biopsy recommended.</p>
            </div>
          )}

          <div className="action-footer">
            <button className="reset-btn" onClick={onReset}>
              Analyze Another Scan
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultCard;
