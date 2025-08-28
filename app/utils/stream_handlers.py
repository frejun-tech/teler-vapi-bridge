import base64
import json
import logging
from typing import List

import numpy as np
from scipy import signal
from teler.streams import StreamOp

from app.core.config import settings

logger = logging.getLogger(__name__)

def resample_audio(audio_data: bytes, from_sr: int = 16000, to_sr: int = 8000) -> bytes:
    """
    High-quality audio downsampling using scipy.decimate for minimal latency and maximum quality.
    
    Args:
        audio_data: Raw PCM audio data as bytes (pcm_s16le format)
        from_sr: Source sample rate (default: 16000 Hz from VAPI)
        to_sr: Target sample rate (default: 8000 Hz for Teler)
    
    Returns:
        Downsampled audio data as bytes (pcm_s16le format at target sample rate)
    """
    try:
        # Convert bytes to numpy array (pcm_s16le format)
        audio_array = np.frombuffer(audio_data, dtype=np.int16)
        
        # Calculate downsampling factor
        factor = from_sr // to_sr  # 16000 // 8000 = 2
        
        # Use scipy.decimate - optimized for integer downsampling with anti-aliasing
        # This method is fast, high quality, and specifically designed for downsampling
        downsampled_array = signal.decimate(
            audio_array, 
            q=factor,      # q=2 for 16kHz->8kHz
            n=8,           # Filter order for high quality
            ftype='iir'    # IIR filter for better performance
        )
        
        # Convert back to 16-bit PCM (pcm_s16le)
        downsampled_int16 = downsampled_array.astype(np.int16)
        
        return downsampled_int16.tobytes()
        
    except Exception as e:
        logger.error(f"Error downsampling audio: {e}")
        # Return original audio if downsampling fails
        return audio_data

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
                    
                    # Convert VAPI audio (pcm_s16le, 16kHz) to Teler format (pcm_s16le, 8kHz)
                    # This ensures smooth audio playback compatibility between the two systems
                    resampled_audio = resample_audio(combined_binary, from_sr=16000, to_sr=8000)
                    
                    # Create payload with same schema as individual messages
                    combined_payload = json.dumps({
                        "type": "audio",
                        "audio_b64": base64.b64encode(resampled_audio).decode('utf-8'),
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
