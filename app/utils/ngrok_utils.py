import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def get_current_ngrok_url() -> Optional[str]:
    """
    Dynamically fetch the current ngrok public URL from ngrok's API
    """
    try:
        # ngrok exposes its API on the ngrok service (port 4040) when running in Docker
        response = requests.get("http://ngrok:4040/api/tunnels", timeout=5)
        if response.status_code == 200:
            tunnels = response.json().get("tunnels", [])
            for tunnel in tunnels:
                if tunnel.get("proto") == "https":
                    public_url = tunnel.get("public_url")
                    if public_url:
                        # Extract just the domain part (remove https://)
                        domain = public_url.replace("https://", "")
                        logger.info(f"Detected ngrok URL: {public_url}")
                        return domain
        else:
            logger.warning(f"Failed to fetch ngrok tunnels: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.warning(f"Could not connect to ngrok API: {e}")
    except Exception as e:
        logger.error(f"Error fetching ngrok URL: {e}")
    
    return None

def get_server_domain() -> str:
    """
    Get the server domain, preferring the dynamic ngrok URL over environment variable
    """
    # Try to get the current ngrok URL first
    ngrok_url = get_current_ngrok_url()
    if ngrok_url:
        return ngrok_url
    
    # Fall back to environment variable if ngrok is not available
    import os
    fallback_domain = os.getenv("SERVER_DOMAIN", "")
    if fallback_domain:
        logger.info(f"Using fallback SERVER_DOMAIN: {fallback_domain}")
        return fallback_domain
    
    logger.warning("No SERVER_DOMAIN available - ngrok may not be running")
    return ""
