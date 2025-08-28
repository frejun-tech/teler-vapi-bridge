import base64
import json
import logging
from typing import Annotated

import httpx
from fastapi import APIRouter, Body, HTTPException, WebSocket, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.core.config import settings
from app.utils.stream_handlers import call_stream_handler, remote_stream_handler
from app.utils.teler_client import TelerClient
from app.utils.vapi_client import VapiClient

logger = logging.getLogger(__name__)
router = APIRouter()

class CallFlowRequest(BaseModel):
    call_id: str
    account_id: str
    from_number: str
    to_number: str

@router.post("/flow", status_code=status.HTTP_200_OK, include_in_schema=False)
async def stream_flow(payload: CallFlowRequest):
    """
    Build and return Stream flow.
    """
    from teler import CallFlow
    
    stream_flow = CallFlow.stream(
        ws_url=f"wss://{settings.server_domain}/api/v1/calls/media-stream",
        chunk_size=500,
        record=True
    )
    return JSONResponse(stream_flow)

@router.get("/initiate-call", status_code=status.HTTP_200_OK)
async def initiate_call():
    """
    Initiate a call using Teler SDK.
    """
    try:
        teler_client = TelerClient(api_key=settings.teler_api_key)
        call = await teler_client.create_call(
            from_number=settings.from_number,
            to_number=settings.to_number,
            flow_url=f"https://{settings.server_domain}/api/v1/calls/flow",
            status_callback_url=f"https://{settings.server_domain}/api/v1/webhooks/receiver",
            record=True,
        )
        logger.info(f"Call created: {call}")
        return JSONResponse(content={"success": True, "call": call})
    except Exception as e:
        logger.error(f"Failed to create call: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Failed to create call."
        )

@router.websocket("/media-stream")
async def handle_media_stream(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket connected.")
    
    try:
        vapi_client = VapiClient(
            api_key=settings.vapi_api_key,
            assistant_id=settings.vapi_assistant_id,
            sample_rate=settings.vapi_sample_rate
        )
        vapi_ws_url = await vapi_client.create_call()
        
        from teler.streams import StreamConnector, StreamType
        
        connector = StreamConnector(
            stream_type=StreamType.BIDIRECTIONAL,
            remote_url=vapi_ws_url,
            call_stream_handler=call_stream_handler,
            remote_stream_handler=remote_stream_handler()
        )
        await connector.bridge_stream(websocket)
    except Exception as e:
        logger.error(f"Error in media stream: {e}")
        await websocket.close()
