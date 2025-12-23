from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi import status
from app.core.config import settings
from app.core.logger import logger


class APIKeyMiddleware(BaseHTTPMiddleware):
    """
    Middleware to validate API Key from request header
    Client must send API Key in header: X-API-Key
    """
    
    # Paths that don't require authentication
    EXCLUDED_PATHS = [
        "/",
        "/health",
        "/docs",
        "/openapi.json",
        "/redoc"
    ]
    
    async def dispatch(self, request: Request, call_next):
        # Skip authentication for excluded paths
        if request.url.path in self.EXCLUDED_PATHS:
            return await call_next(request)
        
        # Get API Key from header
        api_key = request.headers.get("X-API-Key") or request.headers.get("x-api-key")
        
        # Check if API Key is provided
        if not api_key:
            logger.warning(f"Missing API Key for request: {request.url.path}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Missing API Key. Please provide X-API-Key in header."
                }
            )
        
        # Validate API Key
        if api_key != settings.API_KEY:
            logger.warning(f"Invalid API Key for request: {request.url.path}")
            return JSONResponse(
                status_code=status.HTTP_401_UNAUTHORIZED,
                content={
                    "detail": "Invalid API Key"
                }
            )
        
        # API Key is valid, proceed with request
        logger.debug(f"Valid API Key for request: {request.url.path}")
        response = await call_next(request)
        return response