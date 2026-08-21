import sys
import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Ensure the backend directory is in the python path for robust module finding
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from routes import predict, health

app = FastAPI(
    title="Lung Cancer Detection API",
    description="API for detecting lung cancer from CT scan images using a ResNet50 Deep Learning model.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # More permissive for development, can be tightened later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers (modularized for cleaner code)
app.include_router(health.router, prefix="/api", tags=["System Health"])
app.include_router(predict.router, prefix="/api", tags=["Predictions"])

@app.get("/", tags=["Main"])
async def root():
    return {"message": "Welcome to the Lung Cancer Detection API. Visit /docs for interactive documentation."}

if __name__ == "__main__":
    # Run uvicorn on the app object
    uvicorn.run(app, host="0.0.0.0", port=8000)
