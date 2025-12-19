import io
import cv2
import numpy as np
from typing import List
from app.core.logger import logger
from app.services.ocr_service import OCRService
from fastapi.responses import StreamingResponse
from app.dependencies.ocr import get_ocr_service
from app.services.image_service import ImageService
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from app.schemas.ocr import InvoiceFieldsResponse, BBoxListResponse, BBoxResult, MockResponse, ErrorResponse

router = APIRouter()

@router.post("/invoice", response_model=InvoiceFieldsResponse)
async def extract_invoice_fields(file: UploadFile = File(...), ocr_service: OCRService = Depends(get_ocr_service)):
    """
    API 1: Extract invoice fields
    Extracts supplier_name, total, and currency from invoice image.
    Args:
        file: Invoice image file (jpg/png)
    Returns:
        InvoiceFieldsResponse with extracted fields
    """
    try:
        logger.info(f"Processing invoice: {file.filename}")
        
        # Validate and load image
        image = ImageService.validate_image(file)
        
        # Process image through OCR pipeline
        ocr_results = ocr_service.process_image(image)
        
        # Extract invoice fields
        fields = ocr_service.extract_invoice_fields(ocr_results)
        
        logger.info(f"Extracted fields: {fields}")
        
        return InvoiceFieldsResponse(**fields)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing invoice: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing invoice: {str(e)}")

@router.post("/invoice/visualize")
async def visualize_invoice_ocr(file: UploadFile = File(...), ocr_service: OCRService = Depends(get_ocr_service)):
    """
    API 2: OCR with visualization
    Returns image with bounding boxes and recognized text drawn on it.
    Args:
        file: Invoice image file (jpg/png)
    Returns:
        Image with visualization
    """
    try:
        logger.info(f"Visualizing OCR for: {file.filename}")
        
        # Validate and load image
        image = ImageService.validate_image(file)
        
        # Process image through OCR pipeline
        ocr_results = ocr_service.process_image(image)
        
        # Visualize results
        result_image = ocr_service.visualize_results(image, ocr_results)
        
        # Encode image to bytes
        _, img_encoded = cv2.imencode('.png', result_image)
        img_bytes = img_encoded.tobytes()
        
        return StreamingResponse(
            io.BytesIO(img_bytes),
            media_type="image/png",
            headers={"Content-Disposition": f"inline; filename=ocr_result.png"}
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error visualizing OCR: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error visualizing OCR: {str(e)}")

@router.post("/invoice/bboxes", response_model=BBoxListResponse)
async def extract_bboxes(file: UploadFile = File(...), ocr_service: OCRService = Depends(get_ocr_service)):
    """
    API 3: OCR raw bounding boxes
    Returns list of detected text boxes with coordinates and recognized text.
    Args:
        file: Invoice image file (jpg/png)
    Returns:
        BBoxListResponse with list of bounding boxes
    """
    try:
        logger.info(f"Extracting bboxes for: {file.filename}")
        
        # Validate and load image
        image = ImageService.validate_image(file)
        
        # Process image through OCR pipeline
        ocr_results = ocr_service.process_image(image)
        
        # Format results
        bbox_results = []
        for result in ocr_results:
            bbox_results.append(
                BBoxResult(
                    label=result['text'],  # Use text as label
                    text=result['text'],
                    bbox=result['bbox']
                )
            )
        
        logger.info(f"Extracted {len(bbox_results)} bounding boxes")
        
        return BBoxListResponse(results=bbox_results)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error extracting bboxes: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error extracting bboxes: {str(e)}")

@router.get("/mock", response_model=MockResponse)
async def mock_invoice_data():
    """
    API 4: Mock API for testing
    Returns mock invoice data without using models.
    Used for frontend and integration testing.
    Returns:
        MockResponse with sample data
    """
    logger.info("Returning mock data")
    
    return MockResponse(
        supplier_name="ACME Corporation",
        total="12500000",
        currency="VND"
    )
