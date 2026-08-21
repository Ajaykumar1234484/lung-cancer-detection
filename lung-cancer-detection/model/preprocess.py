import os
import cv2
import numpy as np
from PIL import Image

# ==========================================
# Configuration Setup
# ==========================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')

IMG_HEIGHT = 224
IMG_WIDTH = 224

def enhance_contrast_clahe(img_gray):
    """
    Applies Contrast Limited Adaptive Histogram Equalization (CLAHE).
    This is highly effective for medical scans as it enhances local contrast 
    which helps model find tiny tumors/nodules in CT scans.
    """
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(img_gray)

def remove_background(img_gray):
    """
    Applies Gaussian Blur and Otsu's Thresholding to create a mask of the lungs,
    then applies it to remove noise outside the patient's body in the scan.
    """
    # Smoothen the image
    blur = cv2.GaussianBlur(img_gray, (5, 5), 0)
    
    # Apply Otsu's thresholding to isolate lung/tissue vs empty space/background
    _, mask = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Bitwise-AND mask and original image to remove pure black background artifacts if needed
    result = cv2.bitwise_and(img_gray, img_gray, mask=mask)
    return result

def preprocess_image(filepath, target_size=(IMG_HEIGHT, IMG_WIDTH)):
    """
    End-to-end preprocessing pipeline for a single CT image.
    1. Read and convert to grayscale.
    2. Enhance contrast using CLAHE.
    3. Resize.
    4. Convert back to RGB format (required by ResNet50).
    """
    try:
        # Load image as grayscale immediately
        img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
        
        if img is None:
            raise ValueError(f"Image not found or unreadable at {filepath}")
        
        # 1. Enhance Contrast (Crucial for CT scans)
        img_enhanced = enhance_contrast_clahe(img)
        
        # Optional Step 1.5: Remove Background (can be toggled depending on dataset quality)
        # img_enhanced = remove_background(img_enhanced)
        
        # 2. Resize to required dimensions (e.g. 224x224)
        img_resized = cv2.resize(img_enhanced, target_size, interpolation=cv2.INTER_CUBIC)
        
        # 3. Convert grayscale (1 channel) to RGB (3 channels) so it works with ResNet50
        img_rgb = cv2.cvtColor(img_resized, cv2.COLOR_GRAY2RGB)
        
        return img_rgb
        
    except Exception as e:
        print(f"[-] Error processing {filepath}: {e}")
        return None

def process_dataset(source_dir, dest_dir, split_ratio=0.8):
    """
    Reads the raw data directory, processes every image, and saves them
    into train and val subdirectories inside the processed folder based on the split ratio.
    """
    if not os.path.exists(source_dir):
        print(f"[-] Raw data directory {source_dir} not found.")
        print("    Please ensure your raw data is organized inside data/raw/class_name/")
        return
        
    classes = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]
    print(f"Found classes in raw data: {classes}")
    
    # Establish train/val directories
    train_dir = os.path.join(dest_dir, 'train')
    val_dir = os.path.join(dest_dir, 'val')
    
    for c in classes:
        os.makedirs(os.path.join(train_dir, c), exist_ok=True)
        os.makedirs(os.path.join(val_dir, c), exist_ok=True)

    total_processed = 0
    total_failed = 0

    for cls in classes:
        cls_source = os.path.join(source_dir, cls)
        
        files = [f for f in os.listdir(cls_source) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff'))]
        
        # Shuffle files directly for random split
        np.random.shuffle(files)
        
        split_index = int(len(files) * split_ratio)
        train_files = files[:split_index]
        val_files = files[split_index:]
        
        print(f"\nProcessing class '{cls}': {len(train_files)} train, {len(val_files)} val")
        
        # Process Training Files
        for f in train_files:
            img = preprocess_image(os.path.join(cls_source, f))
            if img is not None:
                save_path = os.path.join(train_dir, cls, f)
                cv2.imwrite(save_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
                total_processed += 1
            else:
                total_failed += 1
                
        # Process Validation Files
        for f in val_files:
            img = preprocess_image(os.path.join(cls_source, f))
            if img is not None:
                save_path = os.path.join(val_dir, cls, f)
                cv2.imwrite(save_path, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
                total_processed += 1
            else:
                total_failed += 1

    print("\n==========================================")
    print("Preprocessing Summary:")
    print("==========================================")
    print(f"Successfully processed and split: {total_processed} images")
    print(f"Failed to process: {total_failed} images")
    print(f"Processed dataset saved to: {dest_dir}")

# ==========================================
# Testing block
# ==========================================
if __name__ == "__main__":
    print("Starting preprocessing pipeline...")
    # This prepares the raw images to be eaten by the augmentation script,
    # and eventually, the model's training flow.
    process_dataset(RAW_DATA_DIR, PROCESSED_DATA_DIR, split_ratio=0.8)
