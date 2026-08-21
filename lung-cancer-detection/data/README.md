# Lung Cancer Detection Dataset

This directory contains the image data used to train, validate, and test the Deep Learning model for Lung Cancer Detection. 

Due to size constraints and privacy, the actual DICOM/CT scan images are not included in the version control repository. You must download and place the data here manually.

## Directory Structure

```text
data/
├── README.md               # This file
├── raw/                    # Original, unprocessed CT scans
│   ├── normal/             # Class 0: Healthy scans
│   └── malignant/          # Class 1: Cancerous scans (Tumor/Nodule present)
└── processed/              # Data generated after running model/preprocess.py
    ├── train/              # Training set (80%)
    │   ├── normal/
    │   └── malignant/
    ├── val/                # Validation set (20%)
    │   ├── normal/
    │   └── malignant/
    └── test/               # (Optional) Explicit hold-out set for evaluate.py
```

## How to Get Data
If you don't have a proprietary hospital dataset, you can use public lung cancer datasets such as:
1.  **IQ-OTH/NCCD Lung Cancer Dataset** (Available on Kaggle)
2.  **LUNA16** (Lung Nodule Analysis)
3.  **LIDC-IDRI** (Lung Image Database Consortium image collection)

## Preprocessing Pipeline
**Do not** place files directly into the `processed/` folder. 

1.  Download your dataset (e.g. from Kaggle).
2.  Extract the images (Supported formats: `.jpg`, `.png`, `.tif`).
3.  Organize them into `data/raw/normal/` and `data/raw/malignant/`.
4.  Run the preprocessing script to apply contrast enhancement, resize to $224 \times 224$, and split into Train/Val sets:
    ```bash
    cd ../model/
    python preprocess.py
    ```

Once preprocessing is finished, you can proceed to train the model using `train.py`.
