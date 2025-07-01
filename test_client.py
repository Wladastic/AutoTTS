#!/usr/bin/env python3
"""
Test client for AutoTTS API
"""

import asyncio
import aiohttp
import argparse
import json
from pathlib import Path

class AutoTTSClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def health_check(self):
        """Check server health"""
        async with self.session.get(f"{self.base_url}/health") as response:
            return await response.json()
    
    async def list_models(self):
        """List available models"""
        async with self.session.get(f"{self.base_url}/v1/models") as response:
            return await response.json()
    
    async def list_voices(self):
        """List available voices"""
        async with self.session.get(f"{self.base_url}/v1/voices") as response:
            return await response.json()
    
    async def synthesize_speech(self, text, voice="alloy", model="tts-1", 
                               response_format="mp3", speed=1.0):
        """Synthesize speech"""
        data = {
            "model": model,
            "input": text,
            "voice": voice,
            "response_format": response_format,
            "speed": speed
        }
        
        async with self.session.post(
            f"{self.base_url}/v1/audio/speech",
            json=data
        ) as response:
            if response.status == 200:
                return await response.read()
            else:
                error = await response.json()
                raise Exception(f"API Error: {error}")

async def main():
    parser = argparse.ArgumentParser(description="AutoTTS Test Client")
    parser.add_argument("--url", default="http://localhost:8000", 
                       help="AutoTTS server URL")
    parser.add_argument("--text", default="Hello, this is a test of AutoTTS!",
                       help="Text to synthesize")
    parser.add_argument("--voice", default="alloy",
                       help="Voice to use")
    parser.add_argument("--model", default="tts-1",
                       help="Model to use")
    parser.add_argument("--format", default="mp3",
                       help="Audio format")
    parser.add_argument("--speed", type=float, default=1.0,
                       help="Speech speed")
    parser.add_argument("--output", default="test_output.mp3",
                       help="Output file")
    parser.add_argument("--test-all", action="store_true",
                       help="Run all tests")
    
    args = parser.parse_args()
    
    async with AutoTTSClient(args.url) as client:
        try:
            # Health check
            print("🔍 Checking server health...")
            health = await client.health_check()
            print(f"✅ Server status: {health}")
            print()
            
            if args.test_all:
                # List models
                print("📋 Available models:")
                models = await client.list_models()
                for model in models["data"]:
                    print(f"  - {model['id']}: {model.get('description', 'No description')}")
                print()
                
                # List voices
                print("🎭 Available voices:")
                voices = await client.list_voices()
                for voice in voices["voices"]:
                    print(f"  - {voice['id']} ({voice['name']}): {voice.get('gender', 'unknown')} voice")
                print()
            
            # Synthesize speech
            print(f"🎤 Synthesizing speech...")
            print(f"   Text: {args.text}")
            print(f"   Voice: {args.voice}")
            print(f"   Model: {args.model}")
            print(f"   Format: {args.format}")
            print(f"   Speed: {args.speed}")
            
            audio_data = await client.synthesize_speech(
                text=args.text,
                voice=args.voice,
                model=args.model,
                response_format=args.format,
                speed=args.speed
            )
            
            # Save audio
            output_path = Path(args.output)
            with open(output_path, "wb") as f:
                f.write(audio_data)
            
            print(f"✅ Audio saved to: {output_path}")
            print(f"   Size: {len(audio_data)} bytes")
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return 1
    
    return 0

if __name__ == "__main__":
    exit(asyncio.run(main()))
