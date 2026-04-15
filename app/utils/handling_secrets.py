import hmac
import hashlib
from fastapi import Request, HTTPException
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

def verify_teler_signature(request: Request, raw_body: bytes) -> bool:
    SECRET= settings.SECRET.strip()

    timestamp = request.headers.get("x-teler-timestamp")
    received_signature = request.headers.get("x-teler-signature")

    if not timestamp or not received_signature:
        raise HTTPException(status_code=400, detail="Missing signature headers")

    proto = request.headers.get("x-forwarded-proto", "http")
    host = request.headers.get("x-forwarded-host") or request.headers.get("host")
    path = request.url.path
    signed_url = f"{proto}://{host}{path}"
    method = "POST"

    payload = (
        timestamp.encode()
        + b"|"
        + method.encode()
        + b"|"
        + signed_url.encode()
        + b"|"
        + raw_body
    )

    expected_signature = hmac.new(
        SECRET.encode(),
        payload,
        hashlib.sha256,
    ).hexdigest()

    return hmac.compare_digest(expected_signature, received_signature)
