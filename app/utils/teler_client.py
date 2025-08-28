import logging
from teler import AsyncClient

logger = logging.getLogger(__name__)

class TelerClient:
    """Client for interacting with Teler API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    async def create_call(self, from_number: str, to_number: str, flow_url: str, 
                         status_callback_url: str, record: bool = True):
        """
        Create a call using Teler SDK.
        
        Args:
            from_number: The number to call from
            to_number: The number to call to
            flow_url: URL for the call flow
            status_callback_url: URL for status callbacks
            record: Whether to record the call
            
        Returns:
            The created call object
        """
        try:
            async with AsyncClient(api_key=self.api_key, timeout=10) as client:
                call = await client.calls.create(
                    from_number=from_number,
                    to_number=to_number,
                    flow_url=flow_url,
                    status_callback_url=status_callback_url,
                    record=record,
                )
                logger.info(f"Call created successfully: {call}")
                return call
        except Exception as e:
            logger.error(f"Failed to create call: {e}")
            raise
