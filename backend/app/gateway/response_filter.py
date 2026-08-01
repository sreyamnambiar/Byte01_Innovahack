"""
DarkTrust – API Gateway Response Filter

Injects stringent OWASP-compliant security headers onto outgoing HTTP responses.
"""

from fastapi import Response

class ResponseFilter:
    
    @classmethod
    def filter_response(cls, response: Response) -> Response:
        """
        Applies standard egress security headers to prevent client-side attacks.
        """
        # Prevent browsers from MIME-sniffing a response away from the declared content-type
        response.headers["X-Content-Type-Options"] = "nosniff"
        
        # Prevent clickjacking by denying iframe rendering
        response.headers["X-Frame-Options"] = "DENY"
        
        # Enforce HTTPS strictly on the client side (HSTS) - 1 year duration
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        # Protect against XSS by stopping rendering if an attack is detected
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # Restrict how much referrer information is sent along with requests
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # (Optional) Content Security Policy could be injected here for web clients
        # response.headers["Content-Security-Policy"] = "default-src 'self'"
        
        return response
