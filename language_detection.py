from typing import Optional
import langdetect
from langdetect import detect
import logging

logger = logging.getLogger(__name__)

class LanguageDetector:
    # Language code mapping
    LANGUAGE_MAPPING = {
        'en': 'en',
        'de': 'de', 
        'fr': 'fr',
        'es': 'es',
        'it': 'it',
        'pt': 'pt',
        'ru': 'ru',
        'ja': 'ja',
        'ko': 'ko',
        'zh': 'zh',
        'zh-cn': 'zh',
        'zh-tw': 'zh',
        'ar': 'ar',
        'hi': 'hi',
        'tr': 'tr',
        'pl': 'pl',
        'nl': 'nl',
        'sv': 'sv',
        'da': 'da',
        'no': 'no',
        'fi': 'fi',
        'cs': 'cs',
        'hu': 'hu',
        'ro': 'ro',
        'sk': 'sk',
        'bg': 'bg',
        'hr': 'hr',
        'sl': 'sl',
        'et': 'et',
        'lv': 'lv',
        'lt': 'lt',
        'uk': 'uk',
        'el': 'el',
        'he': 'he',
        'th': 'th',
        'vi': 'vi',
        'id': 'id',
        'ms': 'ms',
        'tl': 'tl',
        'sw': 'sw',
        'am': 'am',
        'mt': 'mt',
        'cy': 'cy',
        'is': 'is',
        'mk': 'mk',
        'sq': 'sq',
        'az': 'az',
        'be': 'be',
        'bn': 'bn',
        'bs': 'bs',
        'ca': 'ca',
        'eu': 'eu',
        'gl': 'gl',
        'ka': 'ka',
        'hy': 'hy',
        'kk': 'kk',
        'ky': 'ky',
        'lo': 'lo',
        'mi': 'mi',
        'mn': 'mn',
        'ne': 'ne',
        'ps': 'ps',
        'fa': 'fa',
        'ta': 'ta',
        'te': 'te',
        'ur': 'ur',
        'uz': 'uz'
    }
    
    def __init__(self):
        self.default_language = 'en'
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of the given text.
        Returns the detected language code or default language if detection fails.
        """
        try:
            # Remove extra whitespace and check if text is meaningful
            text = text.strip()
            if len(text) < 3:
                logger.warning(f"Text too short for reliable language detection: '{text}'")
                return self.default_language
            
            detected_lang = detect(text)
            
            # Map detected language to our supported languages
            if detected_lang in self.LANGUAGE_MAPPING:
                mapped_lang = self.LANGUAGE_MAPPING[detected_lang]
                logger.info(f"Detected language: {detected_lang} -> {mapped_lang}")
                return mapped_lang
            else:
                logger.warning(f"Unsupported language detected: {detected_lang}, using default: {self.default_language}")
                return self.default_language
                
        except Exception as e:
            logger.error(f"Language detection failed: {e}")
            return self.default_language
    
    def is_supported_language(self, lang_code: str) -> bool:
        """Check if a language code is supported"""
        return lang_code.lower() in self.LANGUAGE_MAPPING.values()
    
    def get_supported_languages(self) -> list:
        """Get list of all supported language codes"""
        return list(set(self.LANGUAGE_MAPPING.values()))

language_detector = LanguageDetector()
