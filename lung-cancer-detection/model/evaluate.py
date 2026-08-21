import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# Configuration and Hyperparameters
# ==========================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'processed')
TEST_DIR = os.path.join(DATA_DIR, 'test') # Assuming a separate test set
MODEL_PATH = os.path.join(BASE_DIR, 'model', 'saved_models', 'lung_cancer_model.h5')

IMG_HEIGHT = 224
IMG_WIDTH = 224
BATCH_SIZE = 32

def plot_confusion_matrix(cm, class_names):
    """
    Plots a visually appealing confusion matrix using Seaborn.
    """
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    
    # Save the plot
    save_path = os.path.join(BASE_DIR, 'model', 'confusion_matrix.png')
    plt.savefig(save_path)
    print(f"[+] Confusion matrix saved to: {save_path}")
    plt.close()

def plot_roc_curve(y_true, y_pred_probs):
    """
    Plots the Receiver Operating Characteristic (ROC) curve.
    """
    fpr, tpr, _ = roc_curve(y_true, y_pred_probs)
    roc_auc = auc(fpr, tpr)

    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC)')
    plt.legend(loc="lower right")
    
    # Save the plot
    save_path = os.path.join(BASE_DIR, 'model', 'roc_curve.png')
    plt.savefig(save_path)
    print(f"[+] ROC Curve saved to: {save_path}")
    plt.close()

def evaluate_model():
    """
    Loads the trained model and evaluates it against the test dataset.
    Generates standard classification metrics and visualization plots.
    """
    print("Loading model...")
    if not os.path.exists(MODEL_PATH):
        print(f"[-] Error: Trained model not found at {MODEL_PATH}")
        print("    Please run train.py first to generate the model.")
        return

    try:
        model = load_model(MODEL_PATH)
    except Exception as e:
        print(f"[-] Error loading model: {e}")
        return

    if not os.path.exists(TEST_DIR):
        print(f"[-] Error: Test data directory not found at {TEST_DIR}")
        print("    Please ensure your processed data includes a 'test' split.")
        # Fallback to validation set if test set doesn't exist for demonstration
        val_dir = os.path.join(DATA_DIR, 'val')
        if os.path.exists(val_dir):
            print(f"    [!] Falling back to validation set at {val_dir} for evaluation.")
            eval_dir = val_dir
        else:
            return
    else:
        eval_dir = TEST_DIR

    print(f"Loading evaluation data from: {eval_dir}")
    
    # Test/Val data should strictly ONLY be rescaled, no augmentation
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    # shuffle=False is CRITICAL for linking predictions to true labels/filenames correctly
    test_generator = test_datagen.flow_from_directory(
        eval_dir,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE,
        class_mode='categorical' if model.layers[-1].output_shape[-1] > 2 else 'binary',
        shuffle=False 
    )

    print("\nRunning predictions...")
    # Get raw underlying predictions
    predictions = model.predict(test_generator, verbose=1)
    
    # Determine predicted classes and true classes based on model type
    if test_generator.class_mode == 'categorical':
        y_pred = np.argmax(predictions, axis=1)
        y_true = test_generator.classes
        y_pred_probs = predictions[:, 1] # Assuming class 1 is positive/malignant
    else:
        y_pred = (predictions > 0.5).astype(int).reshape(-1)
        y_true = test_generator.classes
        y_pred_probs = predictions.flatten()
        
    class_names = list(test_generator.class_indices.keys())

    print("\n==========================================")
    print("Classification Report:")
    print("==========================================")
    print(classification_report(y_true, y_pred, target_names=class_names))
    
    print("\n==========================================")
    print("Generating Visualizations...")
    print("==========================================")
    
    # 1. Confusion Matrix
    cm = confusion_matrix(y_true, y_pred)
    plot_confusion_matrix(cm, class_names)
    
    # 2. ROC Curve
    # Note: ROC curve is primarily for binary classification. Multi-class requires One-vs-Rest strategy.
    if len(class_names) == 2:
        plot_roc_curve(y_true, y_pred_probs)
    else:
        print("[!] Note: Standard ROC curve plotted only for binary classification.")
        print("    For multi-class, consider implementing Macro-Average ROC.")

    print("\n[+] Evaluation complete.")

if __name__ == '__main__':
    evaluate_model()
