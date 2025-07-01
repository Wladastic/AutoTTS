#!/usr/bin/env python3
"""
AutoTTS Server - OpenAI-compatible TTS API
"""

import argparse
import asyncio
import uvicorn
from config import settings

def main():
    parser = argparse.ArgumentParser(description="AutoTTS Server")
    parser.add_argument("--host", default=settings.host, help="Host to bind to")
    parser.add_argument("--port", type=int, default=settings.port, help="Port to bind to")
    parser.add_argument("--log-level", default=settings.log_level, 
                       choices=["debug", "info", "warning", "error"], 
                       help="Log level")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    
    args = parser.parse_args()
    
    print("🎤 AutoTTS Server")
    print("================")
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Log Level: {args.log_level}")
    print(f"API Base: {settings.api_base}")
    print("================")
    
    uvicorn.run(
        "main:app",
        host=args.host,
        port=args.port,
        log_level=args.log_level,
        reload=args.reload
    )

if __name__ == "__main__":
    main()
