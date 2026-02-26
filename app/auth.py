# from fastapi import APIRouter, HTTPException, Request
# from fastapi.responses import RedirectResponse
# import msal
# from app.config import CLIENT_ID, CLIENT_SECRET, TENANT_ID, REDIRECT_URI, POWERBI_SCOPE

# router = APIRouter()

# msal_app = msal.ConfidentialClientApplication(
#     CLIENT_ID,
#     authority=f"https://login.microsoftonline.com/{TENANT_ID}",
#     client_credential=CLIENT_SECRET
# )

# @router.get("/login")
# def login(request: Request):
#     request.session.clear()
#     auth_url = msal_app.get_authorization_request_url(
#         scopes=POWERBI_SCOPE,
#         redirect_uri=REDIRECT_URI
#     )
#     return RedirectResponse(auth_url)

# @router.get("/auth/callback")
# def auth_callback(request: Request, code: str):
#     token = msal_app.acquire_token_by_authorization_code(
#         code=code,
#         scopes=POWERBI_SCOPE,
#         redirect_uri=REDIRECT_URI
#     )

#     if "access_token" not in token:
#         raise HTTPException(status_code=400, detail=token)

#     # Store token in session
#     request.session["access_token"] = token["access_token"]
#     request.session["user"] = token.get("id_token_claims")


#     # Redirect to frontend success page
#     return RedirectResponse(
#         "https://id-preview--1115fb10-6ea8-4052-8d1b-31238016c02e.lovable.app/powerbi-auth-success"
#     )

# # newwly added to get detailes
# @router.get("/auth/me")
# def me(request: Request):
#     user = request.session.get("user")
#     if not user:
#         raise HTTPException(status_code=401)

#     return {
#         "name": user.get("name"),
#         "email": user.get("preferred_username"),
#         "oid": user.get("oid"),
#         "tenant": user.get("tid"),
#     }



# from fastapi import APIRouter, HTTPException, Request
# from fastapi.responses import RedirectResponse
# import msal
# from datetime import datetime, timedelta
# from app.config import CLIENT_ID, CLIENT_SECRET, TENANT_ID, REDIRECT_URI, POWERBI_SCOPE

# router = APIRouter()

# msal_app = msal.ConfidentialClientApplication(
#     CLIENT_ID,
#     authority=f"https://login.microsoftonline.com/{TENANT_ID}",
#     client_credential=CLIENT_SECRET
# )

# @router.get("/login")
# def login(request: Request):
#     request.session.clear()
#     auth_url = msal_app.get_authorization_request_url(
#         scopes=POWERBI_SCOPE,
#         redirect_uri=REDIRECT_URI,
#         # Request offline_access to get refresh token
#         prompt="select_account"
#     )
#     return RedirectResponse(auth_url)

# @router.get("/auth/callback")
# def auth_callback(request: Request, code: str):
#     token = msal_app.acquire_token_by_authorization_code(
#         code=code,
#         scopes=POWERBI_SCOPE,
#         redirect_uri=REDIRECT_URI
#     )

#     if "access_token" not in token:
#         raise HTTPException(status_code=400, detail=token)

#     # Store tokens and user info in session
#     request.session["access_token"] = token["access_token"]
#     request.session["refresh_token"] = token.get("refresh_token")  # Store refresh token
#     request.session["user"] = token.get("id_token_claims")
    
#     # Calculate and store token expiry time
#     if "expires_in" in token:
#         expires_at = datetime.now() + timedelta(seconds=token["expires_in"])
#         request.session["token_expires_at"] = expires_at.isoformat()

#     # Redirect to frontend success page
#     return RedirectResponse(
#         "https://id-preview--1115fb10-6ea8-4052-8d1b-31238016c02e.lovable.app/powerbi-auth-success"
#     )

# # Get user details
# @router.get("/auth/me")
# def me(request: Request):
#     user = request.session.get("user")
#     if not user:
#         raise HTTPException(status_code=401, detail="Not authenticated")

#     return {
#         "name": user.get("name"),
#         "email": user.get("preferred_username"),
#         "oid": user.get("oid"),
#         "tenant": user.get("tid"),
#     }

# # Get access token with automatic refresh
# @router.get("/auth/token")
# def get_token(request: Request):
#     access_token = request.session.get("access_token")
#     token_expires_at = request.session.get("token_expires_at")
#     user = request.session.get("user")
    
#     if not access_token:
#         raise HTTPException(status_code=401, detail="Not authenticated")
    
#     # Check if token is expired or about to expire (within 5 minutes)
#     is_expired = False
#     if token_expires_at:
#         expires_at = datetime.fromisoformat(token_expires_at)
#         is_expired = datetime.now() >= (expires_at - timedelta(minutes=5))
    
#     # If expired, try to refresh
#     if is_expired:
#         refresh_token = request.session.get("refresh_token")
#         if not refresh_token:
#             raise HTTPException(status_code=401, detail="Session expired, please login again")
        
#         try:
#             # Refresh the token
#             new_token = msal_app.acquire_token_by_refresh_token(
#                 refresh_token=refresh_token,
#                 scopes=POWERBI_SCOPE
#             )
            
#             if "access_token" not in new_token:
#                 raise HTTPException(status_code=401, detail="Token refresh failed, please login again")
            
#             # Update session with new tokens
#             access_token = new_token["access_token"]
#             request.session["access_token"] = access_token
            
#             if "refresh_token" in new_token:
#                 request.session["refresh_token"] = new_token["refresh_token"]
            
#             if "expires_in" in new_token:
#                 expires_at = datetime.now() + timedelta(seconds=new_token["expires_in"])
#                 request.session["token_expires_at"] = expires_at.isoformat()
                
#         except Exception as e:
#             raise HTTPException(status_code=401, detail=f"Token refresh failed: {str(e)}")
    
#     # Calculate time until expiry
#     expires_in = None
#     if token_expires_at:
#         expires_at = datetime.fromisoformat(token_expires_at)
#         expires_in = int((expires_at - datetime.now()).total_seconds())
    
#     return {
#         "access_token": access_token,
#         "expires_in": expires_in,  # Seconds until expiry
#         "user": {
#             "name": user.get("name") if user else None,
#             "email": user.get("preferred_username") if user else None,
#             "oid": user.get("oid") if user else None,
#             "tenant": user.get("tid") if user else None,
#         } if user else None
#     }

# # Logout endpoint
# @router.post("/auth/logout")
# def logout(request: Request):
#     request.session.clear()
#     return {"message": "Logged out successfully"}

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import RedirectResponse
import msal
from datetime import datetime, timedelta
from app.config import CLIENT_ID, CLIENT_SECRET, TENANT_ID, REDIRECT_URI, POWERBI_SCOPE
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

msal_app = msal.ConfidentialClientApplication(
    CLIENT_ID,
    authority=f"https://login.microsoftonline.com/{TENANT_ID}",
    client_credential=CLIENT_SECRET
)

@router.get("/login")
def login(request: Request):
    request.session.clear()
    auth_url = msal_app.get_authorization_request_url(
        scopes=POWERBI_SCOPE,
        redirect_uri=REDIRECT_URI,
        prompt="select_account"
    )
    return RedirectResponse(auth_url)

@router.get("/auth/callback")
def auth_callback(request: Request, code: str):
    token = msal_app.acquire_token_by_authorization_code(
        code=code,
        scopes=POWERBI_SCOPE,
        redirect_uri=REDIRECT_URI
    )

    if "access_token" not in token:
        logger.error(f"Token acquisition failed: {token}")
        raise HTTPException(status_code=400, detail=token)

    # Store tokens and user info in session
    request.session["access_token"] = token["access_token"]
    request.session["refresh_token"] = token.get("refresh_token")
    request.session["user"] = token.get("id_token_claims")
    
    # Calculate and store token expiry time
    if "expires_in" in token:
        expires_at = datetime.now() + timedelta(seconds=token["expires_in"])
        request.session["token_expires_at"] = expires_at.isoformat()
    
    logger.info(f"User authenticated: {token.get('id_token_claims', {}).get('preferred_username')}")

    return RedirectResponse(
        "https://id-preview--1115fb10-6ea8-4052-8d1b-31238016c02e.lovable.app/powerbi-auth-success"
    )

@router.get("/auth/me")
def me(request: Request):
    user = request.session.get("user")
    if not user:
        logger.warning("Auth/me called without session")
        raise HTTPException(status_code=401, detail="Not authenticated")

    return {
        "name": user.get("name"),
        "email": user.get("preferred_username"),
        "oid": user.get("oid"),
        "tenant": user.get("tid"),
    }

@router.get("/auth/token")
def get_token(request: Request):
    # Log session state for debugging
    logger.info(f"Session keys: {list(request.session.keys())}")
    
    access_token = request.session.get("access_token")
    token_expires_at = request.session.get("token_expires_at")
    user = request.session.get("user")
    
    if not access_token:
        logger.warning("No access token in session")
        raise HTTPException(
            status_code=401, 
            detail="Not authenticated. Please log in again.",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Check if token is expired or about to expire (within 10 minutes)
    is_expired = False
    if token_expires_at:
        expires_at = datetime.fromisoformat(token_expires_at)
        is_expired = datetime.now() >= (expires_at - timedelta(minutes=10))
        logger.info(f"Token expiry check: expires_at={expires_at}, is_expired={is_expired}")
    
    # If expired, try to refresh
    if is_expired:
        refresh_token = request.session.get("refresh_token")
        if not refresh_token:
            logger.warning("No refresh token available")
            raise HTTPException(status_code=401, detail="Session expired, please login again")
        
        try:
            logger.info("Attempting token refresh")
            new_token = msal_app.acquire_token_by_refresh_token(
                refresh_token=refresh_token,
                scopes=POWERBI_SCOPE
            )
            
            if "access_token" not in new_token:
                logger.error(f"Token refresh failed: {new_token}")
                raise HTTPException(status_code=401, detail="Token refresh failed, please login again")
            
            # Update session with new tokens
            access_token = new_token["access_token"]
            request.session["access_token"] = access_token
            
            if "refresh_token" in new_token:
                request.session["refresh_token"] = new_token["refresh_token"]
            
            if "expires_in" in new_token:
                expires_at = datetime.now() + timedelta(seconds=new_token["expires_in"])
                request.session["token_expires_at"] = expires_at.isoformat()
            
            logger.info("Token refreshed successfully")
                
        except Exception as e:
            logger.error(f"Token refresh exception: {str(e)}")
            raise HTTPException(status_code=401, detail=f"Token refresh failed: {str(e)}")
    
    # Calculate time until expiry
    expires_in = None
    if token_expires_at:
        expires_at = datetime.fromisoformat(token_expires_at)
        expires_in = int((expires_at - datetime.now()).total_seconds())
    
    return {
        "access_token": access_token,
        "expires_in": expires_in,
        "user": {
            "name": user.get("name") if user else None,
            "email": user.get("preferred_username") if user else None,
            "oid": user.get("oid") if user else None,
            "tenant": user.get("tid") if user else None,
        } if user else None
    }

# Debug endpoint
@router.get("/auth/session-check")
def session_check(request: Request):
    """Check session status for debugging"""
    has_token = "access_token" in request.session
    has_user = "user" in request.session
    
    return {
        "has_session": has_token or has_user,
        "has_access_token": has_token,
        "has_user": has_user,
        "session_keys": list(request.session.keys()) if request.session else [],
        "timestamp": datetime.now().isoformat()
    }

@router.post("/auth/logout")
def logout(request: Request):
    request.session.clear()
    logger.info("User logged out")
    return {"message": "Logged out successfully"}