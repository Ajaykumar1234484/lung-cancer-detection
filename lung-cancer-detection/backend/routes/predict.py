import io
from fastapi import APIRouter, UploadFile, File, HTTPException
from utils.model_loader import get_model
from utils.image_processing import process_uploaded_image

router = APIRouter()

@router.post("/predict")
async def predict_tumor(file: UploadFile = File(...)):
    """
    Receives a CT scan image, pre-processes it, and runs inference 
    using the loaded trained lung cancer Deep Learning model.
    """
    if file.content_type not in ["image/jpeg", "image/png", "image/tiff"]:
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only JPEG, PNG, and TIFF are supported."
        )
        
    try:
        # Read the uploaded file into memory
        contents = await file.read()
        
        # Load the ML Model via singleton loader
        model = get_model()
        if model is None:
            raise HTTPException(
                status_code=503,
                detail="Machine Learning model is not currently loaded or available."
            )
            
        # Process the raw bytes into a formatted numpy array (224x224 RGB)
        img_array = process_uploaded_image(contents)
        if img_array is None:
            raise HTTPException(
                status_code=422,
                detail="Failed to extract and process image data from upload."
            )
            
        # Run Inference
        prediction = model.predict(img_array)
        
        # Assuming Binary Classification Output (Sigmoid)
        # Class 0: Normal/Benign, Class 1: Malignant
        malignancy_probability = float(prediction[0][0])
        
        is_malignant = malignancy_probability > 0.5
        
        return {
            "prediction": "Malignant" if is_malignant else "Normal",
            "confidence_score": malignancy_probability if is_malignant else (1.0 - malignancy_probability),
            "raw_probability": malignancy_probability,
            "filename": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

@router.post("/treatment-progress")
async def treatment_progress(before_file: UploadFile = File(...), after_file: UploadFile = File(...)):
    """
    Compares two CT scans (before and after treatment) to analyze progress.
    """
    if before_file.content_type not in ["image/jpeg", "image/png", "image/tiff"] or \
       after_file.content_type not in ["image/jpeg", "image/png", "image/tiff"]:
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only JPEG, PNG, and TIFF are supported."
        )

    try:
        model = get_model()
        if model is None:
            raise HTTPException(status_code=503, detail="ML model not available.")

        # Process Before Image
        before_contents = await before_file.read()
        before_img = process_uploaded_image(before_contents)
        before_pred = model.predict(before_img)
        before_prob = float(before_pred[0][0])

        # Process After Image
        after_contents = await after_file.read()
        after_img = process_uploaded_image(after_contents)
        after_pred = model.predict(after_img)
        after_prob = float(after_pred[0][0])

        improvement = (before_prob - after_prob) * 100
        
        status = "Responding well to treatment" if improvement > 10 else \
                 "Stable condition" if improvement > -5 else \
                 "Requires immediate review"

        return {
            "before": {
                "probability": before_prob,
                "percentage": round(before_prob * 100, 1),
                "filename": before_file.filename
            },
            "after": {
                "probability": after_prob,
                "percentage": round(after_prob * 100, 1),
                "filename": after_file.filename
            },
            "improvement": round(improvement, 1),
            "status": status,
            "has_improved": improvement > 0
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")
