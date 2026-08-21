import React from 'react';
import './TreatmentProgress.css';

const TreatmentProgress = ({ progressData, onReset }) => {
  if (!progressData) return null;

  const { before, after, improvement, status, has_improved } = progressData;

  const renderProgressBar = (percentage, label) => {
    // Generate the ASCII-style bar as requested by the user's mock
    const barLength = 20;
    const filledLength = Math.round((percentage / 100) * barLength);
    const bar = '█'.repeat(filledLength) + ' '.repeat(barLength - filledLength);

    return (
      <div className="progress-analysis-row">
        <div className="progress-label">{label}:</div>
        <div className="progress-bar-container">
          <span className="cancer-text">Cancer</span>
          <span className="ascii-bar">{bar}</span>
          <span className="percentage-text">{percentage}%</span>
        </div>
      </div>
    );
  };

  return (
    <div className="treatment-progress-card animate-in">
      <div className="card-header">
        <h2>📊 Treatment Progress Analysis</h2>
      </div>
      
      <div className="card-body">
        {renderProgressBar(before.percentage, 'Before Treatment')}
        {renderProgressBar(after.percentage, 'After Treatment')}

        <div className="comparison-divider"></div>

        <div className="improvement-section">
          <div className="improvement-row">
            <span className="icon">📉</span>
            <span className="label">Improvement:</span>
            <span className={`value ${has_improved ? 'success' : 'warning'}`}>
              {Math.abs(improvement)}% {has_improved ? 'reduction' : 'increase'}
            </span>
          </div>

          <div className="status-row">
            <span className="icon">{has_improved ? '🟢' : '🟡'}</span>
            <span className="label">Status:</span>
            <span className="status-text">{status}</span>
          </div>
        </div>

        <div className="card-footer">
          <button className="reset-btn" onClick={onReset}>
            Start New Analysis
          </button>
        </div>
      </div>
    </div>
  );
};

export default TreatmentProgress;
