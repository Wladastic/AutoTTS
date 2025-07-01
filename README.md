# AutoTTS

🎤 **OpenAI-compatible TTS API with automatic engine selection**

AutoTTS is a modular Text-to-Speech server that automatically chooses the best TTS engine and language based on input text. It provides a fully OpenAI-compatible API that seamlessly integrates with OpenWebUI and other OpenAI-compatible clients.

## Features

- 🔄 **Automatic Engine Selection**: Intelligently chooses the best TTS engine based on language and quality
- 🌍 **Multi-language Support**: Automatic language detection with 50+ supported languages
- 🎭 **Multiple Voices**: Support for various voice types (male, female, neutral)
- 📦 **Modular Architecture**: Easy to add new TTS engines
- 🔌 **OpenAI Compatible**: Drop-in replacement for OpenAI TTS API
- 💾 **Smart Caching**: Reduces latency with intelligent audio caching
- 🚀 **High Performance**: Async/await architecture for concurrent requests

## Supported TTS Engines

- **OuteTTS**: High-quality neural TTS with multilingual support
- **Chatterbox TTS**: Fast and efficient TTS engine
- More engines coming soon...

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/Wladastic/AutoTTS.git
cd AutoTTS

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your preferences
```

### Running the Server

```bash
# Start the server
python server.py

# Or with custom options
python server.py --host 0.0.0.0 --port 8000 --log-level info
```

The server will be available at `http://localhost:8000`

### Testing

```bash
# Test the API
python test_client.py --test-all

# Generate a test audio file
python test_client.py --text "Hello from AutoTTS!" --output hello.mp3
```

## API Endpoints

### OpenAI-Compatible Endpoints

- `POST /v1/audio/speech` - Generate speech from text
- `GET /v1/models` - List available models

### Additional Endpoints

- `GET /health` - Health check
- `GET /v1/voices` - List available voices
- `GET /v1/languages` - List supported languages
- `GET /v1/info` - Server information

## Usage with OpenWebUI

1. In OpenWebUI settings, go to Audio → TTS Settings
2. Set the TTS API URL to: `http://your-autotts-server:8000/v1/audio/speech`
3. Choose any supported voice (alloy, echo, fable, onyx, nova, shimmer)
4. AutoTTS will automatically detect the language and choose the best engine!

## API Usage

### Generate Speech (OpenAI Compatible)

```bash
curl -X POST "http://localhost:8000/v1/audio/speech" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tts-1",
    "input": "Hello, this is AutoTTS speaking!",
    "voice": "alloy",
    "response_format": "mp3",
    "speed": 1.0
  }' \
  --output speech.mp3
```

### List Models

```bash
curl "http://localhost:8000/v1/models"
```

### List Voices

```bash
curl "http://localhost:8000/v1/voices"
```

## Configuration

Create a `.env` file from `.env.example`:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=info

# TTS Engine Configuration
ENABLE_OUTETTS=true
ENABLE_CHATTERBOX=true

# Language Detection
AUTO_DETECT_LANGUAGE=true
DEFAULT_LANGUAGE=en

# Cache Configuration
ENABLE_CACHE=true
CACHE_DIR=./cache
```

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   FastAPI App   │    │   TTS Manager    │    │  Language       │
│                 │    │                  │    │  Detector       │
│ /v1/audio/speech│───▶│ Engine Selection │───▶│                 │
│ /v1/models      │    │ Quality Scoring  │    │ Auto Detection  │
│ /health         │    │ Fallback Logic   │    │ 50+ Languages   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                        ┌──────────────────┐
                        │   TTS Engines    │
                        │                  │
                        │ ┌─────────────┐  │
                        │ │  OuteTTS    │  │
                        │ └─────────────┘  │
                        │ ┌─────────────┐  │
                        │ │ ChatterboxTTS│  │
                        │ └─────────────┘  │
                        │ ┌─────────────┐  │
                        │ │   Future    │  │
                        │ │   Engines   │  │
                        │ └─────────────┘  │
                        └──────────────────┘
```

## Adding New TTS Engines

1. Create a new engine class inheriting from `TTSEngine`
2. Implement the required methods: `initialize()`, `synthesize()`, `get_available_voices()`, etc.
3. Register the engine in `tts_manager.py`
4. Update configuration in `config.py`

Example:

```python
from engines.base import TTSEngine

class MyTTSEngine(TTSEngine):
    def __init__(self, config):
        super().__init__("MyTTS", config)
    
    async def initialize(self):
        # Initialize your TTS engine
        return True
    
    async def synthesize(self, text, voice, language, speed, format):
        # Generate speech
        return audio_bytes
```

## Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
python server.py --reload

# Run tests
python test_client.py --test-all
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add your TTS engine or improvement
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- Inspired by [openedai-speech](https://github.com/matatonic/openedai-speech)
- OuteTTS engine support
- Chatterbox TTS integration
- OpenAI API compatibility

## License
This project is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0).

### Commercial use<br>Companies that wish to use AutoTTS without AGPL obligations can purchase a commercial license. Contact → **github@wlacu.com**
