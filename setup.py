"""
Installation script for OuteTTS integration
"""
import subprocess
import sys
import os
import logging

logger = logging.getLogger(__name__)

def install_outetts():
    """Install OuteTTS from GitHub"""
    try:
        print("🔽 Installing OuteTTS...")
        
        # Clone OuteTTS repository
        subprocess.run([
            "git", "clone", "https://github.com/edwko/OuteTTS.git", "./engines/OuteTTS"
        ], check=True)
        
        # Install OuteTTS dependencies
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-e", "./engines/OuteTTS"
        ], check=True)
        
        print("✅ OuteTTS installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install OuteTTS: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error installing OuteTTS: {e}")
        return False

def install_dependencies():
    """Install additional dependencies for TTS engines"""
    try:
        print("📦 Installing additional dependencies...")
        
        additional_deps = [
            "pydub",           # Audio processing
            "ffmpeg-python",   # Audio format conversion
            "wget",            # File downloading
            "omegaconf",       # Configuration management
            "phonemizer",      # Text phonemization
        ]
        
        for dep in additional_deps:
            subprocess.run([
                sys.executable, "-m", "pip", "install", dep
            ], check=True)
        
        print("✅ Additional dependencies installed!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def main():
    print("🚀 AutoTTS Setup")
    print("================")
    
    # Install additional dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Try to install OuteTTS
    if not install_outetts():
        print("⚠️  OuteTTS installation failed, but you can continue with other engines")
    
    print("\n✅ Setup completed!")
    print("\nNext steps:")
    print("1. Copy .env.example to .env and configure your settings")
    print("2. Run: python server.py")
    print("3. Test with: python test_client.py --test-all")

if __name__ == "__main__":
    main()
