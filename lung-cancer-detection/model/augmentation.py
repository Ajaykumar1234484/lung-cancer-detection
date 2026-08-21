import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img

# ==========================================
# Configuration
# ==========================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw')
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')

IMG_HEIGHT = 224
IMG_WIDTH = 224

# ==========================================
# Augmentation Configuration
# ==========================================
def get_augmenter():
    """
    Returns a configured ImageDataGenerator for standard Medical Image Augmentation.
    """
    return ImageDataGenerator(
        rotation_range=15,          # Degrees range for random rotations
        width_shift_range=0.1,      # Fraction of total width, if < 1
        height_shift_range=0.1,     # Fraction of total height, if < 1
        shear_range=0.1,            # Shear angle in counter-clockwise direction
        zoom_range=0.1,             # Range for random zoom
        horizontal_flip=True,       # Randomly flip inputs horizontally
        vertical_flip=False,        # Vertical flip usually avoided in CT unless axial view justifies it
        fill_mode='nearest',        # Points outside the boundaries of the input are filled
        brightness_range=[0.8, 1.2] # Adjust brightness to simulate different scanners
    )

def augment_image_array(img_array, augmenter, num_variations=5):
    """
    Applies augmentation to a single loaded NumPy image array.
    """
    # Expand dimensions to (1, H, W, C) for the generator
    img_array = np.expand_dims(img_array, axis=0)
    
    iterator = augmenter.flow(img_array, batch_size=1)
    
    augmented_images = []
    for _ in range(num_variations):
        aug_img = next(iterator)[0]  # Get the augmented image as (H, W, C)
        augmented_images.append(aug_img)
        
    return augmented_images

def augment_dataset(source_dir, dest_dir, num_variations=3):
    """
    Iterates through a directory structure (Class folders inside source_dir)
    and saves augmented variations of the images to dest_dir.
    """
    augmenter = get_augmenter()
    
    if not os.path.exists(source_dir):
        print(f"[-] Source directory {source_dir} not found.")
        return
        
    classes = [d for d in os.listdir(source_dir) if os.path.isdir(os.path.join(source_dir, d))]
    
    print(f"Found classes: {classes}")
    
    for cls in classes:
        print(f"Augmenting class: {cls}...")
        cls_source = os.path.join(source_dir, cls)
        cls_dest = os.path.join(dest_dir, cls)
        
        os.makedirs(cls_dest, exist_ok=True)
        
        for filename in os.listdir(cls_source):
            if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tif', '.tiff')):
                continue
                
            filepath = os.path.join(cls_source, filename)
            
            try:
                # Load image and convert to RGB array
                img = load_img(filepath, target_size=(IMG_HEIGHT, IMG_WIDTH))
                img_array = img_to_array(img)
                
                # Save the original image to the destination
                base_name, ext = os.path.splitext(filename)
                orig_dest_path = os.path.join(cls_dest, f"{base_name}_orig{ext}")
                cv2.imwrite(orig_dest_path, cv2.cvtColor(np.uint8(img_array), cv2.COLOR_RGB2BGR))
                
                # Generate and save augmented images
                augmented_imgs = augment_image_array(img_array, augmenter, num_variations)
                
                for i, aug_img in enumerate(augmented_imgs):
                    aug_dest_path = os.path.join(cls_dest, f"{base_name}_aug_{i}{ext}")
                    cv2.imwrite(aug_dest_path, cv2.cvtColor(np.uint8(aug_img), cv2.COLOR_RGB2BGR))
                    
            except Exception as e:
                print(f"[-] Error processing {filename}: {e}")
                
    print(f"[+] Augmentation complete. Data saved to: {dest_dir}")

# ==========================================
# Testing block
# ==========================================
if __name__ == "__main__":
    print("Testing ImageDataGenerator augmentation...")
    # This block allows you to run this script directly to augment the raw data folder
    # into the processed folder immediately.
    
    # You would typically have data/raw/normal and data/raw/malignant
    augment_dataset(RAW_DATA_DIR, os.path.join(PROCESSED_DATA_DIR, 'train'), num_variations=3)
