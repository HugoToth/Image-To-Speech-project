"""Application configuration settings."""

# OCR Settings
TESSERACT_LANGUAGES = 'eng+deu+fra+ita+fin+ron+spa+swe'
IMAGE_CONTRAST_FACTOR = 2.0

# Speech Settings
DEFAULT_SPEECH_RATE = 150
INTERNET_CHECK_URL = "https://www.google.com"
INTERNET_CHECK_TIMEOUT = 3

# UI Settings
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 600
IMAGE_DISPLAY_MIN_HEIGHT = 300

# File Settings
SUPPORTED_IMAGE_FORMATS = "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)"
TEMP_AUDIO_PREFIX = "speech_"
