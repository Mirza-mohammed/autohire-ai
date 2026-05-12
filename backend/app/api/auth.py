from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verifies the JWT token sent from the Next.js frontend.
    In a full production environment, this decodes the token using the NEXTAUTH_SECRET.
    """
    token = credentials.credentials
    
    # MVP Placeholder logic: 
    # Ensure a token is actually present. 
    # If using NextAuth JWTs, use python-jose to decode: `jwt.decode(token, SECRET)`
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Return a dummy user dictionary for MVP downstream endpoints
    return {"id": "user_123", "email": "authenticated@example.com"}
