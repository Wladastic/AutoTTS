import os
import hashlib
from typing import Optional
from config import settings

class CacheManager:
    def __init__(self):
        self.cache_dir = settings.cache_dir
        if settings.enable_cache:
            os.makedirs(self.cache_dir, exist_ok=True)
    
    def get_cache_key(self, text: str, voice: str, model: str, speed: float = 1.0) -> str:
        """Generate a unique cache key for the given parameters"""
        cache_string = f"{text}_{voice}_{model}_{speed}"
        return hashlib.md5(cache_string.encode()).hexdigest()
    
    def get_cache_path(self, cache_key: str, format: str = "mp3") -> str:
        """Get the full path for a cached file"""
        return os.path.join(self.cache_dir, f"{cache_key}.{format}")
    
    def get_cached_audio(self, text: str, voice: str, model: str, speed: float = 1.0, format: str = "mp3") -> Optional[str]:
        """Get cached audio file path if it exists"""
        if not settings.enable_cache:
            return None
        
        cache_key = self.get_cache_key(text, voice, model, speed)
        cache_path = self.get_cache_path(cache_key, format)
        
        if os.path.exists(cache_path):
            return cache_path
        return None
    
    def cache_audio(self, audio_data: bytes, text: str, voice: str, model: str, speed: float = 1.0, format: str = "mp3") -> str:
        """Cache audio data and return the cache path"""
        if not settings.enable_cache:
            return None
        
        cache_key = self.get_cache_key(text, voice, model, speed)
        cache_path = self.get_cache_path(cache_key, format)
        
        with open(cache_path, "wb") as f:
            f.write(audio_data)
        
        return cache_path

cache_manager = CacheManager()
