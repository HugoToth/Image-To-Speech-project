import pyttsx3
import requests
import os
from gtts import gTTS
from playsound import playsound
from PyQt6.QtCore import QThread, pyqtSignal
from utils.logger import setup_logger

logger = setup_logger(__name__)

# --- HELPER FUNCTION 1: INTERNET CHECK ---

def check_internet_connection():
    """
    Checks for a stable internet connection by trying to reach Google.
    :return: True if connected, False otherwise.
    """
    try:
        # We use a short timeout (3s) to avoid long waits
        requests.get("https://www.google.com", timeout=3)
        logger.info("Internet connection found")
        return True
    except (requests.ConnectionError, requests.Timeout):
        logger.info("No internet connection")
        return False

# --- HELPER FUNCTION 2: GET LOCAL VOICES ---

def get_local_voices():
    """
    Gets all installed SAPI 5 voices and returns them as a list of dicts.
    """
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.stop()
        
        voice_list = []
        for voice in voices:
            voice_list.append({
                'name': voice.name,
                'id': voice.id
            })
        logger.info(f"Found {len(voice_list)} local voices")
        return voice_list
    except Exception as e:
        logger.error(f"Error getting local voice list: {e}")
        return []

# --- HELPER FUNCTION 3: GET CLOUD LANGUAGES ---

def get_cloud_languages():
    """
    Returns a curated dictionary of languages for gTTS.
    We are hard-coding the list you provided in your OCR.
    Format: {'Display Name': 'lang_code'}
    """
    return {
        "English": "en",
        "Romanian": "ro",
        "German": "de",
        "French": "fr",
        "Italian": "it",
        "Spanish": "es",
        "Finnish": "fi",
        "Swedish": "sv"
    }

# --- WORKER 1: LOCAL (OFFLINE) TTS ---

class LocalSpeechWorker(QThread):
    """
    A worker thread that runs the local pyttsx3 engine.
    """
    finished = pyqtSignal() 
    error = pyqtSignal(str)

    def __init__(self, text_to_speak: str, voice_id: str):
        super().__init__()
        self.text_to_speak = text_to_speak
        self.voice_id = voice_id
        self.engine = None
        self._should_stop = False

    def run(self):
        try:
            logger.info(f"Starting local speech synthesis")
            self.engine = pyttsx3.init()
            if self.voice_id:
                self.engine.setProperty('voice', self.voice_id)
            self.engine.setProperty('rate', 150)
            self.engine.say(self.text_to_speak)
            self.engine.runAndWait()
            logger.info("Local speech synthesis completed")
        except Exception as e:
            error_msg = f"Error in local speech thread: {e}"
            logger.error(error_msg)
            self.error.emit(error_msg)
        finally:
            if self.engine:
                try:
                    self.engine.stop()
                except:
                    pass
            self.finished.emit()

    def stop(self):
        """Stop the speech playback."""
        self._should_stop = True
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass

# --- WORKER 2: CLOUD (ONLINE) TTS ---

class CloudSpeechWorker(QThread):
    """
    A worker thread that runs the gTTS (Google) engine.
    It saves to a temp file, plays it, and then deletes it.
    """
    finished = pyqtSignal() 
    error = pyqtSignal(str)

    def __init__(self, text_to_speak: str, lang_code: str):
        super().__init__()
        self.text_to_speak = text_to_speak
        self.lang_code = lang_code
        # Define a temp file name. It will be created and deleted.
        self.temp_audio_file = "temp_speech.mp3"
        self._should_stop = False

    def run(self):
        try:
            if self._should_stop:
                return
            
            logger.info(f"Starting cloud speech synthesis (lang: {self.lang_code})")
            
            # 1. Create the gTTS object
            tts = gTTS(text=self.text_to_speak, lang=self.lang_code, slow=False)
            
            # 2. Save the speech to a temporary file
            tts.save(self.temp_audio_file)
            logger.info(f"Audio saved to {self.temp_audio_file}")
            
            if self._should_stop:
                return
            
            # 3. Play the temporary file (this is blocking)
            logger.info("Playing audio...")
            playsound(self.temp_audio_file)
            logger.info("Cloud speech synthesis completed")
            
        except Exception as e:
            error_msg = f"Error in cloud speech thread: {e}"
            logger.error(error_msg)
            self.error.emit(error_msg)
        finally:
            # 4. Clean up: Delete the temporary file
            try:
                if os.path.exists(self.temp_audio_file):
                    os.remove(self.temp_audio_file)
                    logger.info(f"Deleted temp file: {self.temp_audio_file}")
            except Exception as e:
                logger.warning(f"Failed to delete temp file: {e}")
                
            # 5. Signal that we are done
            self.finished.emit()

    def stop(self):
        """Stop the speech playback."""
        logger.info("Stopping cloud speech playback")
        self._should_stop = True
        # Note: playsound doesn't have a simple .stop()
        # The playback will finish the current audio