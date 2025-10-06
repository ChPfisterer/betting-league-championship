"""
Multi-Sport Betting Platform Backend

A FastAPI-based backend service for managing multi-sport betting competitions,
user groups, and real-time rankings with OAuth 2.0 authentication.
"""

import logging
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse

# Add src to Python path
sys.path.append(str(Path(__file__).parent / "src"))

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Import API routers
from api import api_router

# Create FastAPI application
app = FastAPI(
    title="Multi-Sport Betting Platform API",
    description="Comprehensive API for multi-sport betting platform supporting user authentication, group management, sports betting, and real-time rankings.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://localhost:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(api_router)


# Health check endpoint
@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint for monitoring and load balancers."""
    return {
        "status": "healthy",
        "service": "betting-platform-backend",
        "version": "1.0.0",
    }


# Root endpoint
@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint with API information."""
    return {
        "message": "Multi-Sport Betting Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
        },
    )


@app.get("/auth/callback", response_class=HTMLResponse)
async def oauth_callback(
    code: str = Query(..., description="Authorization code from Keycloak"),
    state: str = Query(..., description="State parameter for CSRF protection")
):
    """
    OAuth callback endpoint for testing purposes.
    
    This endpoint receives the authorization code from Keycloak and displays it
    for testing. In a real application, this would be handled by the frontend.
    """
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>OAuth Callback - Testing</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }}
            .container {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
            .success {{ color: #28a745; }}
            .code {{ background: #f8f9fa; padding: 15px; border-radius: 4px; font-family: monospace; word-break: break-all; }}
            .copy-btn {{ background: #007bff; color: white; padding: 8px 16px; border: none; border-radius: 4px; cursor: pointer; margin-top: 10px; }}
            .copy-btn:hover {{ background: #0056b3; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="success">✅ OAuth Login Successful!</h1>
            <p>You have successfully authenticated with Keycloak. Here are the OAuth parameters:</p>
            
            <h3>Authorization Code:</h3>
            <div class="code" id="auth-code">{code}</div>
            <button class="copy-btn" onclick="copyToClipboard('auth-code')">Copy Code</button>
            
            <h3>State:</h3>
            <div class="code" id="state">{state}</div>
            <button class="copy-btn" onclick="copyToClipboard('state')">Copy State</button>
            
            <h3>Next Steps for Testing:</h3>
            <ol>
                <li>Copy the authorization code above</li>
                <li>Use it in the token exchange endpoint:</li>
                <div class="code">
curl -X POST http://localhost:8000/api/v1/auth/keycloak/oauth/token \\
  -H "Content-Type: application/json" \\
  -d '{{
    "code": "{code}",
    "redirect_uri": "http://localhost:8000/auth/callback",
    "state": "{state}"
  }}'
                </div>
            </ol>
        </div>
        
        <script>
            function copyToClipboard(elementId) {{
                const element = document.getElementById(elementId);
                const text = element.textContent;
                navigator.clipboard.writeText(text).then(() => {{
                    alert('Copied to clipboard!');
                }});
            }}
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
