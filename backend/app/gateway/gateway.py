"""
DarkTrust – API Gateway Middleware

The absolute perimeter of the application. 
Intercepts every incoming ASGI request, enforces OWASP validation rules, 
and injects egress security headers onto the response.
"""

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.gateway.request_validator import RequestValidator
from app.gateway.response_filter import ResponseFilter
import time

class GatewayMiddleware(BaseHTTPMiddleware):
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """
        The global interception point.
        """
        start_time = time.time()
        
        # 1. Ingress Validation (Deny malformed or malicious payloads instantly)
        validation_error_response = await RequestValidator.validate_request(request)
        if validation_error_response:
            # Short-circuit the request and return the error before it hits Auth/Routing
            return validation_error_response
            
        # 2. Process Request (Auth -> RBAC -> ZT Policy -> Risk -> Business Logic)
        response = await call_next(request)
        
        # 3. Egress Filtering (Inject strict security headers)
        response = ResponseFilter.filter_response(response)
        
        # 4. Optional metrics injection
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        return response
