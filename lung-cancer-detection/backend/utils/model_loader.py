import os

# Try to import tensorflow, but don't fail if it's not present
try:
    import tensorflow as tf
    from tensorflow.keras.models import load_model
    TF_AVAILABLE = True
except ImportError:
    print("[-] TensorFlow not found. AI Core will run in Simulation Mode.")
    TF_AVAILABLE = False

# Global variable to cache the model in memory
_MODEL_INSTANCE = None

# Path resolution
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'saved_models', 'lung_cancer_model.h5')

class MockModel:
    """A mock model to simulate AI predictions when TensorFlow is unavailable."""
    def predict(self, img_array):
        # Simulate a prediction based on image intensity/variance to feel slightly "real"
        import numpy as np
        # Use filename or something to keep results consistent? Just random for now.
        score = np.random.uniform(0.1, 0.9)
        return [[score]]

def get_model():
    """Returns the loaded Keras model or a Mock model if TF is missing."""
    global _MODEL_INSTANCE
    
    if _MODEL_INSTANCE is None:
        if TF_AVAILABLE:
            try:
                print(f"Loading Lung Cancer Detection model from: {MODEL_PATH}")
                if os.path.exists(MODEL_PATH) and os.path.getsize(MODEL_PATH) > 0:
                    _MODEL_INSTANCE = load_model(MODEL_PATH)
                    print("[+] Model loaded successfully into memory.")
                else:
                    print(f"[-] Model file not found. Falling back to Simulation Mode.")
                    _MODEL_INSTANCE = MockModel()
            except Exception as e:
                print(f"[-] Error loading model: {e}. Falling back to Simulation Mode.")
                _MODEL_INSTANCE = MockModel()
        else:
            _MODEL_INSTANCE = MockModel()
            
    return _MODEL_INSTANCE

def check_model_status():
    """Returns True if a model (real or mock) is available."""
    return get_model() is not None
