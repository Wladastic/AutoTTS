from typing import List, Optional, Literal
from pydantic import BaseModel, Field

class TTSRequest(BaseModel):
    model: str = Field(..., description="The TTS model to use")
    input: str = Field(..., description="The text to convert to speech")
    voice: str = Field(default="alloy", description="The voice to use for synthesis")
    response_format: Optional[Literal["mp3", "opus", "aac", "flac", "wav", "pcm"]] = Field(default="mp3")
    speed: Optional[float] = Field(default=1.0, ge=0.25, le=4.0, description="The speed of the generated audio")

class TTSModel(BaseModel):
    id: str
    object: str = "model"
    created: int
    owned_by: str
    permission: List = []
    root: Optional[str] = None
    parent: Optional[str] = None

class TTSVoice(BaseModel):
    id: str
    name: str
    gender: Optional[str] = None
    language: Optional[str] = None
    engine: str
    description: Optional[str] = None

class ModelsResponse(BaseModel):
    object: str = "list"
    data: List[TTSModel]

class ErrorResponse(BaseModel):
    error: dict
