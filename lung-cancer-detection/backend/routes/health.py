from fastapi import APIRouter
from utils.model_loader import check_model_status

router = APIRouter()

@router.get("/health")
async def health_check():
    """
    Returns the current status of the API and the loaded AI model.
    """
    from utils.model_loader import TF_AVAILABLE
    is_model_ready = check_model_status()
    
    return {
        "status": "online" if is_model_ready else "degraded",
        "api": "ready",
        "model_loaded": is_model_ready,
        "mode": "production" if TF_AVAILABLE else "simulation"
    }
