import sys
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QTextEdit,
                             QFileDialog, QMessageBox, QComboBox)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QTimer

from logic.image_processor import extract_text_from_image
# Import the whole module so we can access all its functions
import logic.speech_synthesizer as tts_logic
from utils.logger import setup_logger
import config

logger = setup_logger(__name__)

class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image-to-Speech Reader")
        self.setMinimumSize(config.WINDOW_MIN_WIDTH, config.WINDOW_MIN_HEIGHT)

        # --- Class Attributes ---
        self.current_image_path = None
        self.speech_thread = None
        self.available_speech_options = {}
        self.is_online = tts_logic.check_internet_connection()

        self._init_ui()
        self._connect_signals()
        self.setup_speech_options()

    def _init_ui(self):
        """Initialize all UI components."""
        self._create_widgets()
        self._create_layouts()
        
    def _create_widgets(self):
        """Create all widgets."""
        # Image display
        self.image_label = QLabel("Please load an image...")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFont(QFont("Arial", 14))
        self.image_label.setStyleSheet("border: 2px dashed #aaa;") 
        self.image_label.setMinimumHeight(config.IMAGE_DISPLAY_MIN_HEIGHT)

        # Text output
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True) 
        self.text_output.setFont(QFont("Arial", 12))
        self.text_output.setPlaceholderText("Extracted text will appear here...")

        # Buttons
        self.load_button = QPushButton("Load Image")
        self.load_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.load_button.setMinimumHeight(40)

        self.read_button = QPushButton("Read Text")
        self.read_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.read_button.setMinimumHeight(40)
        self.read_button.setEnabled(False)

        # Speech controls
        self.speech_label = QLabel()
        self.speech_label.setFont(QFont("Arial", 10))
        
        self.speech_combo_box = QComboBox()
        self.speech_combo_box.setFont(QFont("Arial", 10))
        self.speech_combo_box.setMinimumHeight(40)
        
    def _create_layouts(self):
        """Arrange widgets in layouts."""
        # Speech selector layout
        speech_layout = QVBoxLayout()
        speech_layout.addWidget(self.speech_label)
        speech_layout.addWidget(self.speech_combo_box)
        
        # Bottom controls
        bottom_controls_layout = QHBoxLayout()
        bottom_controls_layout.addWidget(self.load_button, stretch=2)
        bottom_controls_layout.addLayout(speech_layout, stretch=3)
        bottom_controls_layout.addWidget(self.read_button, stretch=2)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.image_label, stretch=2) 
        main_layout.addWidget(self.text_output, stretch=1) 
        main_layout.addLayout(bottom_controls_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
    def _connect_signals(self):
        """Connect all signal-slot pairs."""
        self.load_button.clicked.connect(self.load_image)
        self.read_button.clicked.connect(self.read_text)


    def setup_speech_options(self):
        """
        Populates the speech QComboBox based on internet connectivity.
        """
        if self.is_online:
            logger.info("Setting up in ONLINE mode")
            self.speech_label.setText("Language (Google Cloud):")
            self.available_speech_options = tts_logic.get_cloud_languages()
            self.speech_combo_box.addItems(self.available_speech_options.keys())
            # Select Romanian or English as a default if available
            if "Romanian" in self.available_speech_options:
                self.speech_combo_box.setCurrentText("Romanian")
            elif "English" in self.available_speech_options:
                self.speech_combo_box.setCurrentText("English")
        else:
            logger.info("Setting up in OFFLINE mode")
            self.speech_label.setText("Voice (Local Fallback):")
            voices = tts_logic.get_local_voices()
            if not voices:
                logger.warning("No local voices found")
                self.speech_label.setText("Voice (Offline): NOT FOUND")
                self.read_button.setEnabled(False)
                self.speech_combo_box.setEnabled(False)
                return
            
            # Store as {'Name': 'ID'}
            self.available_speech_options = {v['name']: v['id'] for v in voices}
            self.speech_combo_box.addItems(self.available_speech_options.keys())

    def _set_controls_enabled(self, enabled: bool, speaking: bool = False):
        """
        Enable or disable controls based on application state.
        
        :param enabled: Whether controls should be enabled
        :param speaking: Whether speech is currently active
        """
        self.read_button.setEnabled(enabled and not speaking)
        self.load_button.setEnabled(enabled)
        self.speech_combo_box.setEnabled(enabled and not speaking)

    def read_text(self):
        """Triggers speech synthesis using the appropriate worker."""
        logger.info("'Read Text' button pressed")
        text = self.text_output.toPlainText()
        
        if not self._validate_text(text):
            return
            
        current_option_name = self.speech_combo_box.currentText()
        if not current_option_name:
            QMessageBox.warning(self, "Warning", "Please select a speech option.")
            return
            
        option_value = self.available_speech_options.get(current_option_name)
        if not option_value:
            QMessageBox.warning(self, "Warning", "Invalid speech option selected.")
            return
        
        self._set_controls_enabled(True, speaking=True)
        self._start_speech_thread(text, option_value)
    
    def _validate_text(self, text: str) -> bool:
        """
        Validate that text is suitable for speech synthesis.
        
        :param text: The text to validate
        :return: True if valid, False otherwise
        """
        if not text or "ERROR:" in text or "Processing..." in text:
            QMessageBox.warning(self, "Warning", "No valid text to read.")
            return False
        return True
    
    def _start_speech_thread(self, text: str, option_value: str):
        """
        Start the appropriate speech thread.
        
        :param text: Text to speak
        :param option_value: Language code or voice ID
        """
        if self.is_online:
            logger.info(f"Starting CLOUD speech thread (Lang: {option_value})")
            self.speech_thread = tts_logic.CloudSpeechWorker(text, option_value)
        else:
            logger.info(f"Starting LOCAL speech thread (Voice ID: {option_value})")
            self.speech_thread = tts_logic.LocalSpeechWorker(text, option_value)
        
        # Connect signals for both types
        self.speech_thread.finished.connect(self.on_speech_finished)
        self.speech_thread.error.connect(self.on_speech_error)
        self.speech_thread.start()

    def on_speech_finished(self):
        """Called when the speech thread finishes."""
        logger.info("Speech thread finished")
        self._set_controls_enabled(True, speaking=False)
        self.speech_thread = None

    def on_speech_error(self, error_message: str):
        """
        Called if the speech worker encounters an error.
        
        :param error_message: The error message to display
        """
        logger.error(f"Speech error: {error_message}")
        QMessageBox.critical(self, "Speech Error", error_message)
        
    def load_image(self):
        """Load an image file and trigger OCR processing."""
        logger.info("'Load Image' button pressed")
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select an Image", "", config.SUPPORTED_IMAGE_FORMATS
        )
        if file_path:
            logger.info(f"Image selected: {file_path}")
            self.current_image_path = file_path
            self.display_image()
            self.text_output.setPlainText("Processing... please wait.")
            self.load_button.setEnabled(False)
            self.read_button.setEnabled(False)
            QTimer.singleShot(100, self.run_ocr) 
        else:
            logger.info("User cancelled file selection")

    def run_ocr(self):
        """Process the loaded image with OCR."""
        logger.info("Running OCR")
        try:
            extracted_text = extract_text_from_image(self.current_image_path)
            self.text_output.setPlainText(extracted_text)
            
            # Re-enable controls
            self.load_button.setEnabled(True)
            
            # Enable read button only if we have valid text
            has_valid_text = (
                extracted_text.strip() and 
                "ERROR:" not in extracted_text and
                "No text could be extracted" not in extracted_text
            )
            self.read_button.setEnabled(has_valid_text)
            
            logger.info("OCR Complete")
        except Exception as e:
            error_msg = f"OCR failed: {str(e)}"
            logger.exception(error_msg)
            self.text_output.setPlainText(f"ERROR: {error_msg}")
            self.load_button.setEnabled(True)
            QMessageBox.critical(self, "OCR Error", error_msg)

    def display_image(self):
        if self.current_image_path:
            pixmap = QPixmap(self.current_image_path)
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(), 
                Qt.AspectRatioMode.KeepAspectRatio, 
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
        
    def resizeEvent(self, event):
        self.display_image() 
        super().resizeEvent(event)
        
    def closeEvent(self, event):
        """Handle application close event."""
        logger.info("Application closing")
        event.accept()