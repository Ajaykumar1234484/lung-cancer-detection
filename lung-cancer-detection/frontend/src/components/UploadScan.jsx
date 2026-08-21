import React, { useState, useRef } from 'react';
import { predictScan } from '../api/predict';
import './UploadScan.css';

const UploadScan = ({ onUploadSuccess }) => {
  const [dragActive, setDragActive] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);
  
  const inputRef = useRef(null);

  // Drag and Drop handlers
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelection(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFileSelection(e.target.files[0]);
    }
  };

  const onButtonClick = () => {
    inputRef.current.click();
  };

  const handleFileSelection = (file) => {
    setError(null);
    
    // Validate file type
    const validTypes = ['image/jpeg', 'image/png', 'image/tiff'];
    if (!validTypes.includes(file.type)) {
      setError("Invalid file type. Please upload a JPEG, PNG, or TIFF image.");
      return;
    }

    setSelectedFile(file);
    
    // Create preview
    const objectUrl = URL.createObjectURL(file);
    setPreviewUrl(objectUrl);
  };

  // Keep API call separate or passed as prop, but here's how to trigger the upload
  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setIsUploading(true);
    setError(null);

    try {
      // Use the unified API utility instead of hardcoded fetch
      const data = await predictScan(selectedFile);
      
      if (onUploadSuccess) {
        onUploadSuccess(data, previewUrl);
      }
      
    } catch (err) {
      console.error(err);
      setError(err.message || "Failed to analyze image. Ensure the backend server is running.");
    } finally {
      setIsUploading(false);
    }
  };

  const clearSelection = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setError(null);
    if (inputRef.current) {
      inputRef.current.value = "";
    }
  };

  return (
    <div className="upload-container">
      <h2>Upload CT Scan</h2>
      <p className="upload-subtitle">Supported formats: JPEG, PNG, TIFF</p>

      {!selectedFile ? (
        <div 
          className={`drop-zone ${dragActive ? "drag-active" : ""}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
          onClick={onButtonClick}
        >
          <input
            ref={inputRef}
            type="file"
            accept=".jpg,.jpeg,.png,.tif,.tiff"
            onChange={handleChange}
            style={{ display: "none" }}
          />
          
          <div className="upload-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
              <polyline points="17 8 12 3 7 8"></polyline>
              <line x1="12" y1="3" x2="12" y2="15"></line>
            </svg>
          </div>
          <p>Drag & Drop your scan here</p>
          <span className="or-text">or</span>
          <button className="browse-btn">Browse Files</button>
        </div>
      ) : (
        <div className="preview-container">
          <div className="image-preview">
            <img src={previewUrl} alt="CT Scan Preview" />
          </div>
          
          <div className="file-info">
            <p className="filename">{selectedFile.name}</p>
            <p className="filesize">{(selectedFile.size / (1024 * 1024)).toFixed(2)} MB</p>
          </div>

          <div className="action-buttons">
            <button 
              className="clear-btn" 
              onClick={clearSelection}
              disabled={isUploading}
            >
              Cancel
            </button>
            <button 
              className="analyze-btn" 
              onClick={handleAnalyze}
              disabled={isUploading}
            >
              {isUploading ? "Analyzing..." : "Analyze Scan"}
            </button>
          </div>
        </div>
      )}

      {error && <div className="error-message">{error}</div>}
    </div>
  );
};

export default UploadScan;
