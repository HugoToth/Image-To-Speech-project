import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from utils.logger import setup_logger
import config

logger = setup_logger(__name__)

def extract_text_from_image(image_path: str) -> str:
    """
    Opens an image, pre-processes it for better OCR, and extracts text.
    
    This function handles:
    1. Opening the image.
    2. Pre-processing (grayscale, contrast).
    3. OCR extraction.
    4. Error handling.
    
    :param image_path: The file path to the image.
    :return: The extracted text as a string, or an error message.
    """
    try:
        # Open the image using Pillow
        with Image.open(image_path) as img:
            logger.info(f"Processing image: {image_path}")
            
            # Pre-processing 
            # Convert to grayscale
            processed_img = img.convert('L')
            
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(processed_img)
            processed_img = enhancer.enhance(config.IMAGE_CONTRAST_FACTOR)
            
            # Apply a sharpening filter
            processed_img = processed_img.filter(ImageFilter.SHARPEN)

            # Perform OCR using Tesseract
            text = pytesseract.image_to_string(processed_img, lang=config.TESSERACT_LANGUAGES)
            
            if not text.strip():
                logger.warning("No text extracted from image")
                return "No text could be extracted from this image."
            
            logger.info(f"Successfully extracted {len(text)} characters")
            return text

    except pytesseract.TesseractNotFoundError:
        # This error occurs if Tesseract is not installed or not in the PATH
        error_msg = "Tesseract OCR is not found"
        logger.error(error_msg)
        return (
            "ERROR: Tesseract OCR is not found.\n"
            "Please make sure it is installed and added to your system's PATH."
        )
    except FileNotFoundError:
        error_msg = f"Image file not found at {image_path}"
        logger.error(error_msg)
        return f"ERROR: {error_msg}"
    except Exception as e:
        error_msg = f"An unexpected error occurred: {e}"
        logger.exception(error_msg)
        return f"ERROR: {error_msg}"