import uvicorn
from fastapi import FastAPI
from app.core.logger import logger
from app.core.middleware import APIKeyMiddleware
from app.api.v1.router import api_router
from app.core.config import settings
from contextlib import asynccontextmanager
from app.models.detector import DetectionModel
from app.services.ocr_service import OCRService
from app.models.recognizer import RecognitionModel
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router as api_router_v1

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    Models are loaded once at startup and stored in app.state.
    """
    try:
        logger.info("=" * 60)
        logger.info("Starting OCR API Server")
        logger.info("=" * 60)
        
        # Load Detection Model
        logger.info("Loading Detection Model...")
        det_model = DetectionModel(str(settings.DETECTOR_MODEL_PATH)).load_detection_model()
        logger.info("Detection model loaded successfully")
        
        # Load Recognition Model
        logger.info("Loading Recognition Model...")
        rec_model = RecognitionModel(str(settings.RECOGNIZER_MODEL_PATH)).load_recognition_model()
        logger.info("Recognition model loaded successfully")
        
        # Initialize OCR Service
        logger.info("Initializing OCR Service...")
        app.state.ocr_service = OCRService(det_model, rec_model)
        logger.info("OCR Service initialized")
        
        logger.info("=" * 60)
        logger.info("Server startup completed successfully!") 
        logger.info(f"API Documentation: http://localhost:8000/docs")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"Failed to load models: {e}", exc_info=True)
        raise

    yield

    # Shutdown
    logger.info("Shutting down OCR API Server...")

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.DESCRIPTION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key Authentication Middleware 
app.add_middleware(APIKeyMiddleware)

# Include API router
app.include_router(api_router_v1, prefix=settings.API_V1_PREFIX)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
 