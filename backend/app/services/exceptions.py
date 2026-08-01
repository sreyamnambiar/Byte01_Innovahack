"""
DarkTrust – Service Exceptions

Custom domain exceptions to encapsulate business logic failures.
These keep the service layer decoupled from framework-specific exceptions
(like FastAPI's HTTPException or SQLAlchemy's IntegrityError).
"""

class DarkTrustException(Exception):
    """Base exception for all DarkTrust domain errors."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ResourceNotFoundException(DarkTrustException):
    """Raised when a requested resource (User, Role, etc.) cannot be found."""
    pass

class ResourceAlreadyExistsException(DarkTrustException):
    """Raised when attempting to create a resource that violates a unique constraint."""
    pass

class ValidationException(DarkTrustException):
    """Raised when a business rule validation fails (e.g., assigning an inactive role)."""
    pass
