import pytesseract
from PIL import Image
from io import BytesIO
from typing import BinaryIO

from app.models.schemas import ExtractedText

# Language mapping
LANGUAGES = {
    "english": "eng",
    "italian": "ita",
    "eng": "eng",
    "ita": "ita",
    "en": "eng",
    "it": "ita",
}


def get_lang_code(language: str | None) -> str:
    """Convert language name to Tesseract code."""
    if not language:
        return "eng"
    lang = language.lower().strip()
    if "+" in lang:
        parts = [LANGUAGES.get(p.strip(), p.strip()) for p in lang.split("+")]
        return "+".join(parts)
    return LANGUAGES.get(lang, lang)


def preprocess_image(image: Image.Image) -> Image.Image:
    """Preprocess image for better OCR accuracy."""
    if image.mode != "L":
        image = image.convert("L")

    min_dimension = 300
    if image.width < min_dimension or image.height < min_dimension:
        scale = max(min_dimension / image.width, min_dimension / image.height)
        new_size = (int(image.width * scale), int(image.height * scale))
        image = image.resize(new_size, Image.Resampling.LANCZOS)

    return image


def extract_text(image_file: BinaryIO, filename: str, language: str | None = None) -> ExtractedText:
    """Extract text from image using Tesseract OCR."""
    image_bytes = image_file.read()
    image = Image.open(BytesIO(image_bytes))
    processed_image = preprocess_image(image)

    lang = get_lang_code(language)

    ocr_data = pytesseract.image_to_data(processed_image, lang=lang, output_type=pytesseract.Output.DICT)
    raw_text = pytesseract.image_to_string(processed_image, lang=lang)

    confidences = [conf for conf in ocr_data["conf"] if conf != -1]
    avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

    return ExtractedText(
        filename=filename,
        raw_text=raw_text.strip(),
        confidence=round(avg_confidence, 2)
    )


def extract_from_multiple(image_files: list[tuple[BinaryIO, str]], language: str | None = None) -> list[ExtractedText]:
    """Extract text from multiple images."""
    results = []
    for file, filename in image_files:
        result = extract_text(file, filename, language)
        results.append(result)
    return results
