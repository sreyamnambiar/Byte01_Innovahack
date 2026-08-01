"""
DarkTrust – API Gateway Request Validator

Provides static OWASP-compliant validation methods that scrub incoming HTTP 
requests before they reach the FastAPI routing layer.
"""

from fastapi import Request
from fastapi.responses import JSONResponse

# Max payload size set to 2MB to prevent DoS attacks
MAX_PAYLOAD_SIZE = 2 * 1024 * 1024  

# Allowed API content types
ALLOWED_CONTENT_TYPES = ["application/json", "application/x-www-form-urlencoded", "multipart/form-data"]

class RequestValidator:
    
    @classmethod
    async def validate_request(cls, request: Request) -> JSONResponse | None:
        """
        Executes all inbound validation checks. 
        Returns a JSONResponse error immediately if a check fails, halting the pipeline.
        Returns None if validation passes.
        """
        # 1. Validate payload size
        size_error = await cls.validate_request_size(request)
        if size_error:
            return size_error
            
        # 2. Validate content type (for POST/PUT/PATCH)
        content_error = cls.validate_content_type(request)
        if content_error:
            return content_error
            
        # 3. Validate mandatory headers/API Versioning (if applicable)
        header_error = cls.validate_headers(request)
        if header_error:
            return header_error

        return None

    @classmethod
    async def validate_request_size(cls, request: Request) -> JSONResponse | None:
        """Enforces a strict upper limit on incoming payload bytes."""
        # Note: In ASGI, we can't reliably check Content-Length alone as it can be spoofed.
        # But as a fast pre-check:
        content_length = request.headers.get("content-length")
        if content_length and int(content_length) > MAX_PAYLOAD_SIZE:
            return JSONResponse(status_code=413, content={"detail": "Payload Too Large"})
        return None

    @classmethod
    def validate_content_type(cls, request: Request) -> JSONResponse | None:
        """Ensures the client is sending supported data formats."""
        if request.method in ["POST", "PUT", "PATCH"]:
            content_type = request.headers.get("content-type", "").lower()
            # If no content-type is provided or it doesn't match allowed types (ignoring charset boundary)
            if not content_type:
                return JSONResponse(status_code=415, content={"detail": "Missing Content-Type header"})
                
            is_allowed = any(allowed in content_type for allowed in ALLOWED_CONTENT_TYPES)
            if not is_allowed:
                return JSONResponse(status_code=415, content={"detail": f"Unsupported Media Type: {content_type}"})
                
        return None

    @classmethod
    def validate_headers(cls, request: Request) -> JSONResponse | None:
        """
        Validates mandatory security headers or API versioning.
        Currently ensures the Accept header is present.
        """
        # Example OWASP enforcement
        accept_header = request.headers.get("accept")
        if not accept_header:
            return JSONResponse(status_code=400, content={"detail": "Missing Accept header"})
        
        return None
