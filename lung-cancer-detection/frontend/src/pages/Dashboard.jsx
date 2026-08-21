import React, { useState, useEffect } from 'react';
import UploadScan from '../components/UploadScan';
import ResultCard from '../components/ResultCard';
import HeatmapViewer from '../components/HeatmapViewer';
import TreatmentProgress from '../components/TreatmentProgress';
import { checkSystemHealth, getTreatmentProgress } from '../api/predict';
import './Dashboard.css';

const Dashboard = () => {
  const [predictionData, setPredictionData] = useState(null);
  const [progressData, setProgressData] = useState(null);
  const [scanImage, setScanImage] = useState(null);
  const [backendStatus, setBackendStatus] = useState('checking');
  const [analysisMode, setAnalysisMode] = useState('single'); // 'single' or 'progress'
  
  // States for progress mode uploads
  const [beforeFile, setBeforeFile] = useState(null);
  const [afterFile, setAfterFile] = useState(null);
  const [isAnalyzingProgress, setIsAnalyzingProgress] = useState(false);
  const [progressError, setProgressError] = useState(null);

  // Verify the Python API and Deep Learning Model are online before allowing uploads
  useEffect(() => {
    const verifySystemState = async () => {
      const health = await checkSystemHealth();
      setBackendStatus(health.model_loaded ? 'online' : 'offline');
    };
    
    verifySystemState();
  }, []);

  // Called when UploadScan successfully gets a result from the backend
  const handleAnalysisSuccess = (data, imageUrl) => {
    setPredictionData(data);
    setScanImage(imageUrl);
  };

  // Called to clear the current results and start over
  const handleReset = () => {
    setPredictionData(null);
    setProgressData(null);
    setScanImage(null);
    setBeforeFile(null);
    setAfterFile(null);
    setProgressError(null);
    // Smooth scroll back to top of the dashboard
    window.scrollTo({ top: 0, left: 0, behavior: 'smooth' });
  };

  const handleProgressAnalysis = async () => {
    if (!beforeFile || !afterFile) return;
    
    setIsAnalyzingProgress(true);
    setProgressError(null);
    
    try {
      const data = await getTreatmentProgress(beforeFile, afterFile);
      setProgressData(data);
    } catch (err) {
      setProgressError(err.message || "Failed to analyze treatment progress.");
    } finally {
      setIsAnalyzingProgress(false);
    }
  };

  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <h1>Radiology Dashboard</h1>
        <div className={`system-status ${backendStatus}`}>
          <span className="status-indicator"></span>
          {backendStatus === 'online' ? 'System Online: AI Core Loaded' : 
           backendStatus === 'checking' ? 'Connecting to Core...' : 'System Offline: Backend Unavailable'}
        </div>
      </div>

      <div className="mode-toggle-container">
        <button 
          className={`mode-btn ${analysisMode === 'single' ? 'active' : ''}`}
          onClick={() => { setAnalysisMode('single'); handleReset(); }}
        >
          Single Scan Analysis
        </button>
        <button 
          className={`mode-btn ${analysisMode === 'progress' ? 'active' : ''}`}
          onClick={() => { setAnalysisMode('progress'); handleReset(); }}
        >
          Treatment Progress Analysis
        </button>
      </div>

      {!predictionData && !progressData ? (
        <div className="dashboard-upload-section">
          {analysisMode === 'single' ? (
            <>
              <p className="instruction-text">
                Upload a high-resolution Axial CT scan format (.jpg, .png, .tif) to begin analysis.
                The ResNet50 core will process the image for Malignant nodule patterns.
              </p>
              <UploadScan onUploadSuccess={handleAnalysisSuccess} />
            </>
          ) : (
            <div className="progress-upload-container">
              <p className="instruction-text">
                Upload two CT scans (Before and After treatment) to analyze therapeutic response and tumor reduction.
              </p>
              
              <div className="dual-upload-grid">
                <div className="upload-box">
                  <h3>1. Before Treatment</h3>
                  <input 
                    type="file" 
                    onChange={(e) => setBeforeFile(e.target.files[0])}
                    className="file-input-simple"
                  />
                  {beforeFile && <p className="selected-filename">✓ {beforeFile.name}</p>}
                </div>
                
                <div className="upload-box">
                  <h3>2. After Treatment</h3>
                  <input 
                    type="file" 
                    onChange={(e) => setAfterFile(e.target.files[0])}
                    className="file-input-simple"
                  />
                  {afterFile && <p className="selected-filename">✓ {afterFile.name}</p>}
                </div>
              </div>

              <div className="progress-actions">
                <button 
                  className="analyze-progress-btn"
                  onClick={handleProgressAnalysis}
                  disabled={!beforeFile || !afterFile || isAnalyzingProgress}
                >
                  {isAnalyzingProgress ? "Analyzing Therapeutic Data..." : "Run Progress Analysis"}
                </button>
                {progressError && <p className="error-text">{progressError}</p>}
              </div>
            </div>
          )}
          
          {backendStatus === 'offline' && (
            <div className="backend-warning">
              <strong>Warning:</strong> The FastAPI backend server is not reachable or the model weights 
              (<code>lung_cancer_model.h5</code>) are missing. Please ensure <code>python app.py</code> is running.
            </div>
          )}
        </div>
      ) : (
        <div className="dashboard-results-section fade-in">
          {analysisMode === 'single' ? (
            <>
              <ResultCard 
                predictionData={predictionData} 
                imageUrl={scanImage} 
                onReset={handleReset} 
              />
              <HeatmapViewer 
                originalImage={scanImage}
                heatmapImage={predictionData.heatmap_url || null} 
              />
            </>
          ) : (
            <TreatmentProgress 
              progressData={progressData} 
              onReset={handleReset} 
            />
          )}
        </div>
      )}
    </div>
  );
};

export default Dashboard;
