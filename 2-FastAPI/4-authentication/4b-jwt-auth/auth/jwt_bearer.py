"""
JWT Bearer Token Dependency

Validates Bearer tokens in Authorization header.
"""

from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from .jwt_handler import decode_token


class JWTBearer(HTTPBearer):
    """
    Custom HTTPBearer that validates JWT tokens.
    
    Usage:
        @app.get("/protected")
        def protected_route(current_user = Depends(JWTBearer())):
            ...
    """
    
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
    
    async def __call__(self, request) -> Optional[str]:
        """
        Validate the JWT token in the Authorization header.
        
        Expected format: Authorization: Bearer <token>
        """
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        
        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or missing credentials"
            )
        
        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme"
            )
        
        # Verify the token
        token = credentials.credentials
        payload = decode_token(token)
        
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token"
            )
        
        return payload
