import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.applications import ResNet50

def generate_dummy_model():
    """
    Creates an initialized, untrained model matching the train.py architecture
    so that the backend API can be tested before actual training is complete.
    """
    print("Building dummy model...")
    # Using ResNet50 pre-trained on ImageNet as the feature extractor
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # We don't need compilation or dropout since we're just saving weights for the backend to test inference
    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dense(256, activation='relu'),
        Dense(1, activation='sigmoid') # Assuming binary classification (Normal/Malignant)
    ])
    
    # The empty file was created by the python setup script but is not a valid h5.
    # We must overwrite it with an actual keras structure.
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    save_path = os.path.join(base_dir, 'model', 'saved_models', 'lung_cancer_model.h5')
    
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    model.save(save_path)
    print(f"\n[+] Successfully saved untrained dummy model to: {save_path}")
    print("    This allows the backend API to load a valid format. Please run train.py to generate real weights later.")

if __name__ == "__main__":
    generate_dummy_model()
