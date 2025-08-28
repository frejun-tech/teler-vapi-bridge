import logging
from typing import Annotated

from fastapi import APIRouter, Body, status
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/receiver", status_code=status.HTTP_200_OK, include_in_schema=False)
async def webhook_receiver(data: Annotated[dict, Body()]):
    """
    Log webhook payload from Teler.
    """
    logger.info(f"--------Webhook Payload-------- {data}")
    return JSONResponse(content="Webhook received.")
