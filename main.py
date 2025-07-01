import logging
import time
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import io
from typing import Optional

from models import TTSRequest, ModelsResponse, TTSModel, ErrorResponse
from tts_manager import tts_manager
from cache import cache_manager
from config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    # Startup
    logger.info("Starting AutoTTS server...")
    try:
        await tts_manager.initialize()
        logger.info("AutoTTS server started successfully")
    except Exception as e:
        logger.error(f"Failed to start AutoTTS server: {e}")
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down AutoTTS server...")
    await tts_manager.cleanup()

# Create FastAPI app
app = FastAPI(
    title="AutoTTS",
    description="OpenAI-compatible TTS API with automatic engine selection",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests"""
    start_time = time.time()
    
    # Log request
    logger.info(f"{request.method} {request.url.path} - Client: {request.client.host}")
    
    response = await call_next(request)
    
    # Log response
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - Time: {process_time:.3f}s")
    
    return response

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "AutoTTS - OpenAI-compatible TTS API",
        "version": "1.0.0",
        "engines": list(tts_manager.engines.keys()) if tts_manager.initialized else [],
        "endpoints": {
            "models": "/v1/models",
            "speech": "/v1/audio/speech",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if not tts_manager.initialized:
        raise HTTPException(status_code=503, detail="TTS engines not initialized")
    
    return {
        "status": "healthy",
        "engines": len(tts_manager.engines),
        "engines_list": list(tts_manager.engines.keys())
    }

@app.get(f"{settings.api_base}/models", response_model=ModelsResponse)
async def list_models():
    """List available TTS models (OpenAI compatible)"""
    try:
        models = tts_manager.get_available_models()
        return ModelsResponse(data=[TTSModel(**model) for model in models])
    except Exception as e:
        logger.error(f"Error listing models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post(f"{settings.api_base}/audio/speech")
async def create_speech(request: TTSRequest):
    """Generate speech from text (OpenAI compatible)"""
    try:
        logger.info(f"Speech request: model={request.model}, voice={request.voice}, "
                   f"format={request.response_format}, speed={request.speed}")
        
        # Check cache first
        cached_path = cache_manager.get_cached_audio(
            text=request.input,
            voice=request.voice,
            model=request.model,
            speed=request.speed,
            format=request.response_format
        )
        
        if cached_path:
            logger.info("Serving from cache")
            return StreamingResponse(
                io.BytesIO(open(cached_path, "rb").read()),
                media_type=f"audio/{request.response_format}",
                headers={"X-Cache": "HIT"}
            )
        
        # Generate new audio
        audio_data = await tts_manager.synthesize(
            text=request.input,
            voice=request.voice,
            speed=request.speed,
            format=request.response_format,
            model=request.model
        )
        
        # Cache the result
        if settings.enable_cache:
            cache_manager.cache_audio(
                audio_data=audio_data,
                text=request.input,
                voice=request.voice,
                model=request.model,
                speed=request.speed,
                format=request.response_format
            )
        
        # Return audio response
        return StreamingResponse(
            io.BytesIO(audio_data),
            media_type=f"audio/{request.response_format}",
            headers={"X-Cache": "MISS"}
        )
        
    except Exception as e:
        logger.error(f"Speech generation failed: {e}")
        error_detail = str(e)
        
        # Return OpenAI-compatible error
        error_response = {
            "error": {
                "message": error_detail,
                "type": "invalid_request_error",
                "code": "audio_generation_failed"
            }
        }
        return JSONResponse(
            status_code=500,
            content=error_response
        )

@app.get(f"{settings.api_base}/voices")
async def list_voices():
    """List available voices (extension to OpenAI API)"""
    try:
        voices = tts_manager.get_available_voices()
        return {"voices": voices}
    except Exception as e:
        logger.error(f"Error listing voices: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get(f"{settings.api_base}/languages")
async def list_languages():
    """List supported languages (extension to OpenAI API)"""
    try:
        languages = tts_manager.get_supported_languages()
        return {"languages": languages}
    except Exception as e:
        logger.error(f"Error listing languages: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get(f"{settings.api_base}/info")
async def get_info():
    """Get server information"""
    return {
        "server": "AutoTTS",
        "version": "1.0.0",
        "engines": list(tts_manager.engines.keys()) if tts_manager.initialized else [],
        "cache_enabled": settings.enable_cache,
        "auto_language_detection": settings.auto_detect_language,
        "supported_formats": ["mp3", "wav", "opus", "aac", "flac", "pcm"],
        "api_base": settings.api_base
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level,
        reload=True
    )
