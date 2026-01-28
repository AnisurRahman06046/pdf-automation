import pytesseract
from PIL import Image
from io import BytesIO
from typing import BinaryIO

from app.models.schemas import ExtractedText


def preprocess_image(image: Image.Image) -> Image.Image:
    """Preprocess image for better OCR accuracy."""
    # Convert to grayscale
    if image.mode != "L":
        image = image.convert("L")

    # Resize if too small (OCR works better with larger images)
    min_dimension = 300
    if image.width < min_dimension or image.height < min_dimension:
        scale = max(min_dimension / image.width, min_dimension / image.height)
        new_size = (int(image.width * scale), int(image.height * scale))
        image = image.resize(new_size, Image.Resampling.LANCZOS)

    return image


def extract_text(image_file: BinaryIO, filename: str) -> ExtractedText:
    """Extract text from a single image using Tesseract OCR."""
    image_bytes = image_file.read()
    image = Image.open(BytesIO(image_bytes))

    # Preprocess for better accuracy
    processed_image = preprocess_image(image)

    # Get OCR data with confidence
    ocr_data = pytesseract.image_to_data(processed_image, output_type=pytesseract.Output.DICT)

    # Extract text
    raw_text = pytesseract.image_to_string(processed_image)

    # Calculate average confidence (excluding -1 which means no text detected)
    confidences = [conf for conf in ocr_data["conf"] if conf != -1]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

    return ExtractedText(
        filename=filename,
        raw_text=raw_text.strip(),
        confidence=round(avg_confidence, 2)
    )


def extract_from_multiple(image_files: list[tuple[BinaryIO, str]]) -> list[ExtractedText]:
    """Extract text from multiple images."""
    results = []
    for file, filename in image_files:
        result = extract_text(file, filename)
        results.append(result)
    return results
