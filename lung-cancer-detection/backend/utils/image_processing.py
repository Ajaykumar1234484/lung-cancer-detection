import cv2
import numpy as np

def enhance_contrast_clahe(img_gray):
    """
    Matches the preprocessing step used during model training.
    """
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(img_gray)

def process_uploaded_image(file_bytes, target_size=(224, 224)):
    """
    Takes raw bytes from a FastAPI UploadFile, decodes it into an OpenCV image,
    runs the identical preprocessing pipeline from model/preprocess.py,
    and returns a normalized NumPy array ready for model.predict().
    """
    try:
        # Decode image from raw bytes
        np_arr = np.frombuffer(file_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            return None
            
        # 1. Enhance Contrast
        img_enhanced = enhance_contrast_clahe(img)
        
        # 2. Resize
        img_resized = cv2.resize(img_enhanced, target_size, interpolation=cv2.INTER_CUBIC)
        
        # 3. Convert to 3-Channel RGB (Required by ResNet50)
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_GRAY2RGB)
        
        # 4. Normalize (Since we used ImageDataGenerator(rescale=1./255) during training)
        img_normalized = img_rgb.astype('float32') / 255.0
        
        # 5. Expand dims for batch size: (224, 224, 3) -> (1, 224, 224, 3)
        img_batch = np.expand_dims(img_normalized, axis=0)
        
        return img_batch
        
    except Exception as e:
        print(f"[-] Image processing error: {e}")
        return None
