import os

from pydantic_settings import BaseSettings
from app.utils.ngrok_utils import get_server_domain


class Settings(BaseSettings):
    """Application settings"""
    
    # VAPI Configuration
    vapi_api_key: str = os.getenv("VAPI_API_KEY", "")
    vapi_assistant_id: str = os.getenv("VAPI_ASSISTANT_ID", "")
    vapi_sample_rate: int = int(os.getenv("VAPI_SAMPLE_RATE", "16000"))
    vapi_message_buffer_size: int = int(os.getenv("VAPI_MESSAGE_BUFFER_SIZE", "50"))
    
    # Server Configuration - dynamically get ngrok URL
    @property
    def server_domain(self) -> str:
        return get_server_domain()
    
    server_host: str = os.getenv("SERVER_HOST", "0.0.0.0")
    server_port: int = int(os.getenv("SERVER_PORT", "8000"))
    
    # Teler Configuration
    teler_api_key: str = os.getenv("TELER_API_KEY", "")
    from_number: str = os.getenv("FROM_NUMBER", "+91123*******")
    to_number: str = os.getenv("TO_NUMBER", "+91456*******")
    
    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance
settings = Settings()
