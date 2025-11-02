# Image-to-Speech Reader

A PyQt6-based desktop application that extracts text from images using OCR (Optical Character Recognition) and converts it to speech using either cloud-based (Google TTS) or local text-to-speech engines.

## Features

- **Image Loading** - Support for PNG, JPG, JPEG, BMP, and TIFF formats
- **Multi-language OCR** - Extracts text in English, Romanian, German, French, Italian, Spanish, Finnish, and Swedish
- **Hybrid TTS** - Automatically switches between online (Google TTS) and offline (pyttsx3) modes
- **Multiple Voices** - Choose from various languages (online) or installed voices (offline)
- **Text Editor** - View and edit extracted text before reading
- **Clean UI** - Modern, user-friendly interface built with PyQt6
- **Logging** - Clean console output for debugging

## Requirements

- Python 3.8+
- Tesseract OCR (must be installed separately and added to PATH)

## Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Image-To-Speech-project
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install Tesseract OCR:**
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Install and add to system PATH
   - Verify installation: `tesseract --version`

## Usage

1. **Run the application:**
   ```bash
   python app.py
   ```

2. **Load an image:**
   - Click "Load Image" button
   - Select an image file containing text
   - Wait for OCR processing to complete

3. **Read the text:**
   - Select a voice/language from the dropdown
   - Click "Read Text" to start speech synthesis
   - Audio will play automatically when ready

## Project Structure

```
Image-To-Speech-project/
├── app.py                      # Main application entry point
├── config.py                   # Configuration settings
├── requirements.txt            # Python dependencies
├── gui/
│   └── main_window.py         # Main window UI and logic
├── logic/
│   ├── image_processor.py     # OCR functionality
│   └── speech_synthesizer.py # TTS workers and helpers
└── utils/
    ├── logger.py              # Logging configuration
    └── check_voices.py        # Voice checking utility
```

## Configuration

Edit `config.py` to customize:
- OCR languages
- Image processing parameters
- Speech synthesis settings
- UI dimensions

## Features in Detail

### OCR Processing
- Automatic image preprocessing (grayscale, contrast enhancement, sharpening)
- Multi-language support configurable via `config.py`
- Error handling for missing Tesseract installation

### Speech Synthesis
- **Online Mode** (requires internet):
  - Uses Google Text-to-Speech (gTTS)
  - High-quality voices in multiple languages
  - Automatic temp file management
  
- **Offline Mode** (no internet required):
  - Uses pyttsx3 with SAPI 5 voices
  - Works with locally installed Windows voices
  - Fallback when internet is unavailable

### User Interface
- Responsive layout that adapts to window resizing
- Visual feedback for all operations
- Error messages with helpful instructions
- Disabled controls during speech playback

## Troubleshooting

### "Tesseract OCR is not found"
- Ensure Tesseract is installed
- Add Tesseract to system PATH
- Restart the application

### "No local voices found"
- Install Windows SAPI 5 voices
- Check voice availability with `python utils/check_voices.py`

### Audio playback issues
- Check system audio settings and volume
- Ensure `playsound` package is installed
- Try both online and offline modes
- For offline mode, verify SAPI 5 voices are installed on Windows

## Dependencies

- **PyQt6** - GUI framework
- **pytesseract** - OCR wrapper for Tesseract
- **Pillow** - Image processing library
- **gTTS** - Google Text-to-Speech API
- **pyttsx3** - Local text-to-speech engine
- **playsound** - Simple audio playback
- **requests** - HTTP client for connectivity checks

## Author

Hugo Toth
