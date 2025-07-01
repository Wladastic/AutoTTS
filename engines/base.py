from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
import logging

logger = logging.getLogger(__name__)

class TTSEngine(ABC):
    """Abstract base class for TTS engines"""
    
    def __init__(self, name: str, config: Dict[str, Any] = None):
        self.name = name
        self.config = config or {}
        self.is_initialized = False
        self.supported_languages = []
        self.supported_voices = []
        self.supported_formats = ["mp3", "wav"]
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the TTS engine"""
        pass
    
    @abstractmethod
    async def synthesize(self, text: str, voice: str = "default", language: str = "en", 
                        speed: float = 1.0, format: str = "mp3") -> bytes:
        """Synthesize speech from text"""
        pass
    
    @abstractmethod
    def get_available_voices(self) -> List[Dict[str, str]]:
        """Get list of available voices"""
        pass
    
    @abstractmethod
    def get_supported_languages(self) -> List[str]:
        """Get list of supported languages"""
        pass
    
    def supports_language(self, language: str) -> bool:
        """Check if engine supports given language"""
        return language.lower() in [lang.lower() for lang in self.supported_languages]
    
    def supports_voice(self, voice: str) -> bool:
        """Check if engine supports given voice"""
        return voice in [v["id"] for v in self.supported_voices]
    
    def supports_format(self, format: str) -> bool:
        """Check if engine supports given format"""
        return format.lower() in [fmt.lower() for fmt in self.supported_formats]
    
    def get_quality_score(self, language: str, voice: str) -> float:
        """Get quality score for language/voice combination (0.0-1.0)"""
        # Default implementation - can be overridden by engines
        if not self.supports_language(language):
            return 0.0
        if not self.supports_voice(voice):
            return 0.5  # Can use default voice
        return 0.8  # Good quality if both supported
    
    async def cleanup(self):
        """Cleanup resources"""
        pass
