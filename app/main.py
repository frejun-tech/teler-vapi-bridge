import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router
from app.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create FastAPI app
app = FastAPI(
    title="Teler VAPI Bridge",
    description="A bridge application between Teler and VAPI for voice calls using media streaming.",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include router
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Teler VAPI Bridge is running", 
        "status": "healthy",
        "server_domain": settings.server_domain
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "teler-vapi-bridge"}

@app.get("/ngrok-status")
async def ngrok_status():
    """Get current ngrok status and URL"""
    from app.utils.ngrok_utils import get_current_ngrok_url
    current_url = get_current_ngrok_url()
    return {
        "ngrok_running": current_url is not None,
        "current_ngrok_url": f"https://{current_url}" if current_url else None,
        "server_domain": settings.server_domain,
        "fallback_domain": getattr(settings, '_server_domain_fallback', None)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
