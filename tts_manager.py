import logging
from typing import Dict, List, Optional, Tuple
from engines.base import TTSEngine
from engines.outetts import OuteTTSEngine
from engines.chatterbox import ChatterboxTTSEngine
from language_detection import language_detector
from config import settings

logger = logging.getLogger(__name__)

class TTSManager:
    """Manages multiple TTS engines and automatically selects the best one"""
    
    def __init__(self):
        self.engines: Dict[str, TTSEngine] = {}
        self.initialized = False
    
    async def initialize(self):
        """Initialize all enabled TTS engines"""
        logger.info("Initializing TTS Manager...")
        
        # Initialize OuteTTS if enabled
        if settings.enable_outetts:
            try:
                outetts_config = {
                    "device": settings.outetts_device,
                    "model_path": settings.outetts_model_path
                }
                outetts = OuteTTSEngine(outetts_config)
                if await outetts.initialize():
                    self.engines["outetts"] = outetts
                    logger.info("OuteTTS engine registered")
                else:
                    logger.warning("Failed to initialize OuteTTS")
            except Exception as e:
                logger.error(f"Error initializing OuteTTS: {e}")
        
        # Initialize Chatterbox TTS if enabled
        if settings.enable_chatterbox:
            try:
                chatterbox_config = {
                    "device": settings.chatterbox_device,
                    "model_path": settings.chatterbox_model_path
                }
                chatterbox = ChatterboxTTSEngine(chatterbox_config)
                if await chatterbox.initialize():
                    self.engines["chatterbox"] = chatterbox
                    logger.info("ChatterboxTTS engine registered")
                else:
                    logger.warning("Failed to initialize ChatterboxTTS")
            except Exception as e:
                logger.error(f"Error initializing ChatterboxTTS: {e}")
        
        if not self.engines:
            raise RuntimeError("No TTS engines could be initialized")
        
        self.initialized = True
        logger.info(f"TTS Manager initialized with {len(self.engines)} engines: {list(self.engines.keys())}")
    
    def select_best_engine(self, text: str, voice: str = "alloy", language: Optional[str] = None) -> Tuple[TTSEngine, str]:
        """
        Select the best TTS engine for given parameters
        Returns (engine, detected_language)
        """
        if not self.initialized:
            raise RuntimeError("TTS Manager not initialized")
        
        # Detect language if not provided
        if language is None and settings.auto_detect_language:
            language = language_detector.detect_language(text)
        elif language is None:
            language = settings.default_language
        
        logger.info(f"Selecting engine for language: {language}, voice: {voice}")
        
        # Score all engines
        best_engine = None
        best_score = 0.0
        
        for engine_name, engine in self.engines.items():
            score = engine.get_quality_score(language, voice)
            logger.debug(f"Engine {engine_name} score: {score}")
            
            if score > best_score:
                best_score = score
                best_engine = engine
        
        if best_engine is None:
            # Fallback to first available engine
            best_engine = next(iter(self.engines.values()))
            logger.warning(f"No optimal engine found, using fallback: {best_engine.name}")
        else:
            logger.info(f"Selected engine: {best_engine.name} (score: {best_score})")
        
        return best_engine, language
    
    async def synthesize(self, text: str, voice: str = "alloy", language: Optional[str] = None, 
                        speed: float = 1.0, format: str = "mp3", model: str = "tts-1") -> bytes:
        """Synthesize speech using the best available engine"""
        engine, detected_language = self.select_best_engine(text, voice, language)
        
        try:
            audio_data = await engine.synthesize(
                text=text,
                voice=voice,
                language=detected_language,
                speed=speed,
                format=format
            )
            
            logger.info(f"Successfully synthesized audio using {engine.name}")
            return audio_data
            
        except Exception as e:
            logger.error(f"Synthesis failed with {engine.name}: {e}")
            
            # Try with other engines as fallback
            for engine_name, fallback_engine in self.engines.items():
                if fallback_engine != engine:
                    try:
                        logger.info(f"Trying fallback engine: {engine_name}")
                        audio_data = await fallback_engine.synthesize(
                            text=text,
                            voice=voice,
                            language=detected_language,
                            speed=speed,
                            format=format
                        )
                        logger.info(f"Fallback synthesis successful with {engine_name}")
                        return audio_data
                    except Exception as fallback_error:
                        logger.error(f"Fallback engine {engine_name} also failed: {fallback_error}")
                        continue
            
            # If all engines failed
            raise RuntimeError(f"All TTS engines failed to synthesize speech: {e}")
    
    def get_available_models(self) -> List[Dict]:
        """Get all available models from all engines"""
        models = []
        
        # Add standard OpenAI-compatible models
        base_models = [
            {
                "id": "tts-1",
                "object": "model",
                "created": 1699046015,
                "owned_by": "autotts",
                "description": "Standard quality TTS model"
            },
            {
                "id": "tts-1-hd",
                "object": "model", 
                "created": 1699046015,
                "owned_by": "autotts",
                "description": "High definition TTS model"
            }
        ]
        
        models.extend(base_models)
        
        # Add engine-specific models
        for engine_name, engine in self.engines.items():
            engine_model = {
                "id": f"tts-1-{engine_name}",
                "object": "model",
                "created": 1699046015,
                "owned_by": "autotts",
                "description": f"TTS model using {engine.name} engine"
            }
            models.append(engine_model)
        
        return models
    
    def get_available_voices(self) -> List[Dict]:
        """Get all available voices from all engines"""
        all_voices = []
        voice_ids = set()
        
        for engine in self.engines.values():
            for voice in engine.get_available_voices():
                if voice["id"] not in voice_ids:
                    all_voices.append(voice)
                    voice_ids.add(voice["id"])
        
        return all_voices
    
    def get_supported_languages(self) -> List[str]:
        """Get all supported languages from all engines"""
        all_languages = set()
        
        for engine in self.engines.values():
            all_languages.update(engine.get_supported_languages())
        
        return sorted(list(all_languages))
    
    async def cleanup(self):
        """Cleanup all engines"""
        for engine in self.engines.values():
            await engine.cleanup()

# Global TTS manager instance
tts_manager = TTSManager()
