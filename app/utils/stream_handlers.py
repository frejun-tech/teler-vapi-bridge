import base64
import json
import logging
from typing import List, Tuple, Any

from app.core.config import settings
from teler.streams import StreamOp

logger = logging.getLogger(__name__)

async def call_stream_handler(message: str):
    """
    Handle incoming websocket messages from Teler.
    """
    try:
        msg = json.loads(message)
        if msg["type"] == "audio":
            payload = base64.b64decode(msg["data"]["audio_b64"].encode('utf-8'))
            return (payload, StreamOp.RELAY)
        return ({}, StreamOp.PASS)
    except Exception as e:
        logger.error(f"Error in call stream handler: {e}")
        return ({}, StreamOp.PASS)

def remote_stream_handler():
    """
    Handle incoming websocket messages from Vapi.
    """
    chunk_id = 1
    message_buffer: List[bytes] = []  # Just store the binary audio data

    async def handler(message: str):
        nonlocal chunk_id
        try:
            if isinstance(message, bytes):
                # Store just the binary data
                message_buffer.append(message)
                
                # Check if buffer is full
                if len(message_buffer) >= settings.vapi_message_buffer_size:
                    logger.info(f"Buffer full ({len(message_buffer)} messages), relaying combined audio to Teler")
                    
                    # Combine all binary audio data into one continuous segment
                    combined_binary = b''.join(message_buffer)
                    
                    # Create payload with same schema as individual messages
                    combined_payload = json.dumps({
                        "type": "audio",
                        "audio_b64": base64.b64encode(combined_binary).decode('utf-8'),
                        "chunk_id": chunk_id,
                    })
                    
                    # Clear buffer after relaying
                    message_buffer.clear()
                    
                    # Increment chunk_id only when relaying
                    chunk_id += 1
                    
                    # Relay the combined payload
                    return (combined_payload, StreamOp.RELAY)
                else:
                    # Buffer not full yet, don't relay
                    logger.debug(f"Buffered message, buffer size: {len(message_buffer)}/{settings.vapi_message_buffer_size}")
                    return ({}, StreamOp.PASS)
            else:
                logger.info(f"VAPI Control: {message}")
                return ({}, StreamOp.PASS)
        except Exception as e:
            logger.error(f"Error in remote stream handler: {e}")
            return ({}, StreamOp.PASS)

    return handler
