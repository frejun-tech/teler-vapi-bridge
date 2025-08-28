import logging
import httpx

logger = logging.getLogger(__name__)

class VapiClient:
    """Client for interacting with VAPI API"""
    
    def __init__(self, api_key: str, assistant_id: str, sample_rate: int = 8000):
        self.api_key = api_key
        self.assistant_id = assistant_id
        self.sample_rate = sample_rate
        self.base_url = "https://api.vapi.ai"
    
    async def create_call(self) -> str:
        """
        Create a VAPI call and return the WebSocket URL.
        
        Returns:
            WebSocket URL for the VAPI call
            
        Raises:
            Exception: If call creation fails
        """
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    f"{self.base_url}/call",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "assistantId": self.assistant_id,
                        "transport": {
                            "provider": "vapi.websocket",
                            "audioFormat": {
                                "format": "pcm_s16le",
                                "container": "raw",
                                "sampleRate": self.sample_rate
                            }
                        }
                    }
                )
                response.raise_for_status()
                
                data = response.json()
                websocket_url = data.get("transport", {}).get("websocketCallUrl")
                
                if not websocket_url:
                    raise Exception("No WebSocket URL returned from VAPI")
                
                logger.info(f"VAPI call created successfully: {websocket_url}")
                return websocket_url
                
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error creating VAPI call: {e.response.status_code} - {e.response.text}")
            raise Exception(f"Failed to create VAPI call: HTTP {e.response.status_code}")
        except Exception as e:
            logger.error(f"Error creating VAPI call: {e}")
            raise
