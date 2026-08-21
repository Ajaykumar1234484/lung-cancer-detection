import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, GlobalAveragePooling2D
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator


# Configuration and Hyperparameters
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')
MODEL_SAVE_PATH = os.path.join(BASE_DIR, 'model', 'saved_models', 'lung_cancer_model.h5')

IMG_HEIGHT = 224
IMG_WIDTH = 224
BATCH_SIZE = 32
EPOCHS = 50
NUM_CLASSES = 2  # Assuming binary classification (e.g., Normal vs. Malignant)
LEARNING_RATE = 1e-4


# Model Definition

def create_model(input_shape=(IMG_HEIGHT, IMG_WIDTH, 3), num_classes=NUM_CLASSES):
    """
    Creates and compiles a CNN model for lung cancer detection using Transfer Learning (ResNet50).
    """
    print("Building model...")
    # Using ResNet50 pre-trained on ImageNet as the feature extractor
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=input_shape)
    
    # Freeze the base model layers initially
    base_model.trainable = False
    
    model = Sequential([
        base_model,
        GlobalAveragePooling2D(),
        Dense(256, activation='relu'),
        Dropout(0.5),
        # Output layer formulation based on number of classes
        Dense(num_classes if num_classes > 2 else 1, 
              activation='softmax' if num_classes > 2 else 'sigmoid')
    ])
    
    loss_fn = 'categorical_crossentropy' if num_classes > 2 else 'binary_crossentropy'
    class_mode = 'categorical' if num_classes > 2 else 'binary'
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
        loss=loss_fn,
        metrics=['accuracy', tf.keras.metrics.AUC(name='auc')]
    )
    
    return model, class_mode

# Training Pipeline

def main():
    print(f"TensorFlow Version: {tf.__version__}")
    
    train_dir = os.path.join(DATA_DIR, 'train')
    val_dir = os.path.join(DATA_DIR, 'val')
    
    # Check if directories exist
    if not os.path.exists(train_dir) or not os.path.exists(val_dir):
        print(f"[-] Error: Training or validation data directory not found.")
        print(f"    Expected: {train_dir} and {val_dir}")
        print(f"    Please run the preprocessing script to organize your data first.")
        return

    # Define Data Generators with Augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    
    # Validation data should only be rescaled, not augmented
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    # Determine class mode from model creation
    model, class_mode_info = create_model()
    model.summary()
    
    print("Loading data...")
    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode=class_mode_info
    )
    
    val_generator = val_datagen.flow_from_directory(
        val_dir,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode=class_mode_info
    )
    
    # Ensure save directory exists
    os.makedirs(os.path.dirname(MODEL_SAVE_PATH), exist_ok=True)
    
    # Callbacks
    checkpoint = ModelCheckpoint(
        MODEL_SAVE_PATH,
        monitor='val_loss',
        save_best_only=True,
        verbose=1
    )
    
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        verbose=1
    )
    
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.2,
        patience=5,
        min_lr=1e-6,
        verbose=1
    )
    
    print("\nStarting training...")
    try:
        history = model.fit(
            train_generator,
            epochs=EPOCHS,
            validation_data=val_generator,
            callbacks=[checkpoint, early_stopping, reduce_lr]
        )
        print(f"\n[+] Training complete. Best model saved to: {MODEL_SAVE_PATH}")
    except KeyboardInterrupt:
        print("\n[-] Training interrupted by user. Best model up to this point may be saved if it hit a checkpoint.")

if __name__ == '__main__':
    main()
