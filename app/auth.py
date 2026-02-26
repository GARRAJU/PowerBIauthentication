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

router = APIRouter()

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
        # Request offline_access to get refresh token
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
        raise HTTPException(status_code=400, detail=token)

    # Store tokens and user info in session
    request.session["access_token"] = token["access_token"]
    request.session["refresh_token"] = token.get("refresh_token")  # Store refresh token
    request.session["user"] = token.get("id_token_claims")
    
    # Calculate and store token expiry time
    if "expires_in" in token:
        expires_at = datetime.now() + timedelta(seconds=token["expires_in"])
        request.session["token_expires_at"] = expires_at.isoformat()

    # Redirect to frontend success page
    return RedirectResponse(
        "https://id-preview--1115fb10-6ea8-4052-8d1b-31238016c02e.lovable.app/powerbi-auth-success"
    )

# Get user details
@router.get("/auth/me")
def me(request: Request):
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    return {
        "name": user.get("name"),
        "email": user.get("preferred_username"),
        "oid": user.get("oid"),
        "tenant": user.get("tid"),
    }

# Get access token with automatic refresh
@router.get("/auth/token")
def get_token(request: Request):
    access_token = request.session.get("access_token")
    token_expires_at = request.session.get("token_expires_at")
    user = request.session.get("user")
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Check if token is expired or about to expire (within 10 minutes) - CHANGED FROM 5 TO 10
    is_expired = False
    if token_expires_at:
        expires_at = datetime.fromisoformat(token_expires_at)
        is_expired = datetime.now() >= (expires_at - timedelta(minutes=10))  # ← CHANGED HERE
    
    # If expired, try to refresh
    if is_expired:
        refresh_token = request.session.get("refresh_token")
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Session expired, please login again")
        
        try:
            # Refresh the token
            new_token = msal_app.acquire_token_by_refresh_token(
                refresh_token=refresh_token,
                scopes=POWERBI_SCOPE
            )
            
            if "access_token" not in new_token:
                raise HTTPException(status_code=401, detail="Token refresh failed, please login again")
            
            # Update session with new tokens
            access_token = new_token["access_token"]
            request.session["access_token"] = access_token
            
            if "refresh_token" in new_token:
                request.session["refresh_token"] = new_token["refresh_token"]
            
            if "expires_in" in new_token:
                expires_at = datetime.now() + timedelta(seconds=new_token["expires_in"])
                request.session["token_expires_at"] = expires_at.isoformat()
                
        except Exception as e:
            raise HTTPException(status_code=401, detail=f"Token refresh failed: {str(e)}")
    
    # Calculate time until expiry
    expires_in = None
    if token_expires_at:
        expires_at = datetime.fromisoformat(token_expires_at)
        expires_in = int((expires_at - datetime.now()).total_seconds())
    
    return {
        "access_token": access_token,
        "expires_in": expires_in,  # Seconds until expiry
        "user": {
            "name": user.get("name") if user else None,
            "email": user.get("preferred_username") if user else None,
            "oid": user.get("oid") if user else None,
            "tenant": user.get("tid") if user else None,
        } if user else None
    }

# Logout endpoint
@router.post("/auth/logout")
def logout(request: Request):
    request.session.clear()
    return {"message": "Logged out successfully"}