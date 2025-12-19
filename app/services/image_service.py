import cv2
import numpy as np
from fastapi import UploadFile, HTTPException

class ImageService:    

    def validate_image(file: UploadFile) -> np.ndarray:
        """Validate and load image from upload file"""
        # Check content type if available
        if file.content_type and not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read image
        contents = file.file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        return image