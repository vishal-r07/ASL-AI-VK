#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Text-to-Speech Utility

This module provides a simple interface for text-to-speech conversion using Google's
Text-to-Speech (gTTS) library, with support for multiple languages.
"""

import os
import tempfile
import logging
from gtts import gTTS
import pygame

class TextToSpeech:
    """
    A class to handle text-to-speech conversion and playback.
    """
    def __init__(self):
        """
        Initializes the TextToSpeech engine.
        """
        self.last_spoken_text = None

    def speak(self, text, lang='en', slow=False):
        """
        Converts the given text to speech and plays it.

        Args:
            text (str): The text to be spoken.
            lang (str): The language of the text (e.g., 'en' for English, 'hi' for Hindi).
            slow (bool): Whether to speak the text slowly.
        """
        if not text or text == self.last_spoken_text:
            logging.debug(f"Skipping TTS for repeated or empty text: '{text}'")
            return

        temp_filename = None
        try:
            logging.info(f"Generating speech for: '{text}' in language: {lang}")
            tts = gTTS(text=text, lang=lang, slow=slow)
            
            # Use a temporary file to store and play the audio
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_filename = fp.name
                tts.save(temp_filename)
            
            # Use pygame for playback (pure Python, reliable on Windows)
            pygame.mixer.init()
            pygame.mixer.music.load(temp_filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.unload()
            self.last_spoken_text = text

        except Exception as e:
            logging.error(f"Error in text-to-speech: {e}")
        finally:
            # Clean up the temporary file
            if temp_filename and os.path.exists(temp_filename):
                os.remove(temp_filename)
