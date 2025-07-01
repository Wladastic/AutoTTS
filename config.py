import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "info"
    
    # API configuration
    api_base: str = "/v1"
    default_voice: str = "alloy"
    default_model: str = "tts-1"
    
    # TTS Engine configuration
    enable_outetts: bool = True
    enable_chatterbox: bool = True
    
    # OuteTTS configuration
    outetts_model_path: Optional[str] = None
    outetts_device: str = "auto"  # auto, cpu, cuda
    
    # Chatterbox TTS configuration
    chatterbox_model_path: Optional[str] = None
    chatterbox_device: str = "auto"
    
    # Language detection
    auto_detect_language: bool = True
    default_language: str = "en"
    
    # Audio output configuration
    output_format: str = "mp3"  # mp3, wav, opus
    sample_rate: int = 24000
    
    # Cache configuration
    enable_cache: bool = True
    cache_dir: str = "./cache"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
