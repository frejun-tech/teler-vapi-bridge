import logging
from fastapi import APIRouter, status, Request, HTTPException
from fastapi.responses import JSONResponse
from app.utils.handling_secrets import verify_teler_signature

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/receiver", status_code=status.HTTP_200_OK, include_in_schema=False)
async def webhook_receiver(request: Request, data: dict):
    raw_body = await request.body()
    is_valid = verify_teler_signature(request, raw_body)

    if not is_valid:
        logger.error("Invalid webhook signature")
        logger.error("RAW BODY: %r", raw_body)
        raise HTTPException(status_code=401, detail="Invalid signature")

    logger.info("Webhook signature verified")
    logger.info(f"--------Webhook Payload--------\n{data}")

    return JSONResponse(content="Webhook received")
