/**
 * Utility functions for making HTTP requests to the FastAPI backend.
 * Base URL defaults to localhost:8000 for local development.
 */
const API_BASE_URL = import.meta.env?.VITE_API_URL || 'http://localhost:8000/api';

/**
 * Sends a CT scan image to the backend for Lung Cancer prediction.
 * 
 * @param {File} imageFile - The image file from the input/drag-and-drop.
 * @returns {Promise<Object>} The prediction data {prediction, confidence_score, filename}.
 * @throws {Error} If the server responds with a non-2xx status code.
 */
export const predictScan = async (imageFile) => {
  if (!imageFile) {
    throw new Error('No image file provided for prediction.');
  }

  const formData = new FormData();
  formData.append('file', imageFile);

  try {
    const response = await fetch(`${API_BASE_URL}/predict`, {
      method: 'POST',
      body: formData,
      // Note: Do NOT set 'Content-Type' header when sending FormData.
      // The browser automatically sets it to 'multipart/form-data' with the correct boundary.
    });

    if (!response.ok) {
      // Attempt to parse JSON error message from FastAPI if it exists
      const errorData = await response.json().catch(() => null);
      if (errorData && errorData.detail) {
         throw new Error(`Server Error: ${errorData.detail}`);
      }
      throw new Error(`HTTP Error ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
    
  } catch (error) {
    console.error('Prediction API Error:', error);
    // Rethrow to allow the calling component (like UploadScan.jsx) to handle the UI state
    throw error;
  }
};

/**
 * Checks the health status of the backend API and ML model.
 * Useful for displaying system status on the Dashboard before a user tries to upload.
 * 
 * @returns {Promise<Object>} The health status {status, api, model_loaded}.
 */
export const checkSystemHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    });

    if (!response.ok) {
      return { status: "offline", api: "offline", model_loaded: false };
    }

    const data = await response.json();
    return data;

  } catch (error) {
    console.error('Health Check API Error:', error);
    return { status: "offline", api: "error", model_loaded: false };
  }
};

/**
 * Sends two CT scan images (before and after) to the backend for Treatment Progress Analysis.
 * 
 * @param {File} beforeFile - The "before" treatment image file.
 * @param {File} afterFile - The "after" treatment image file.
 * @returns {Promise<Object>} The progress data {before, after, improvement, status, has_improved}.
 */
export const getTreatmentProgress = async (beforeFile, afterFile) => {
  if (!beforeFile || !afterFile) {
    throw new Error('Both before and after images are required for progress analysis.');
  }

  const formData = new FormData();
  formData.append('before_file', beforeFile);
  formData.append('after_file', afterFile);

  try {
    const response = await fetch(`${API_BASE_URL}/treatment-progress`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      if (errorData && errorData.detail) {
         throw new Error(`Server Error: ${errorData.detail}`);
      }
      throw new Error(`HTTP Error ${response.status}: ${response.statusText}`);
    }

    return await response.json();
    
  } catch (error) {
    console.error('Treatment Progress API Error:', error);
    throw error;
  }
};
