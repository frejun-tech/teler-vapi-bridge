from fastapi import APIRouter

from app.api.endpoints import calls, webhooks

# Create main router
router = APIRouter()

# Include endpoint routers
router.include_router(calls.router, prefix="/calls", tags=["calls"])
router.include_router(webhooks.router, prefix="/webhooks", tags=["webhooks"])
