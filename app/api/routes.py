from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import Response
from io import BytesIO
import json

from app.config import ALLOWED_IMAGE_EXTENSIONS, ALLOWED_PDF_EXTENSION
from app.models.schemas import (
    HealthResponse,
    PDFFieldsResponse,
    OCRResponse,
    ParsedOCRResponse,
)
from app.services import pdf_service, ocr_service, parser_service

router = APIRouter()


def validate_pdf(file: UploadFile) -> None:
    """Validate that the uploaded file is a PDF."""
    if not file.filename.lower().endswith(ALLOWED_PDF_EXTENSION):
        raise HTTPException(status_code=400, detail="File must be a PDF")


def validate_image(file: UploadFile) -> None:
    """Validate that the uploaded file is an image."""
    ext = "." + file.filename.lower().split(".")[-1] if "." in file.filename else ""
    if ext not in ALLOWED_IMAGE_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid image format. Allowed: {', '.join(ALLOWED_IMAGE_EXTENSIONS)}"
        )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="ok", message="PDF Automation API is running")


@router.post("/api/pdf/fields", response_model=PDFFieldsResponse)
async def get_pdf_fields(pdf_file: UploadFile = File(...)):
    """
    Upload a PDF to discover all fillable form fields.

    Returns a list of field names and their types.
    """
    validate_pdf(pdf_file)

    try:
        fields = pdf_service.get_form_fields(pdf_file.file)
        return PDFFieldsResponse(
            filename=pdf_file.filename,
            field_count=len(fields),
            fields=fields
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@router.post("/api/ocr/extract", response_model=OCRResponse)
async def extract_text_from_images(images: list[UploadFile] = File(...)):
    """
    Extract text from uploaded images using OCR.

    Accepts one or more image files.
    """
    for image in images:
        validate_image(image)

    try:
        image_files = [(img.file, img.filename) for img in images]
        results = ocr_service.extract_from_multiple(image_files)
        return OCRResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR Error: {str(e)}")


@router.post("/api/ocr/extract-parsed", response_model=ParsedOCRResponse)
async def extract_and_parse_images(images: list[UploadFile] = File(...)):
    """
    Extract text from images and parse structured data (names, dates, IDs, etc.).
    """
    for image in images:
        validate_image(image)

    try:
        image_files = [(img.file, img.filename) for img in images]
        results = ocr_service.extract_from_multiple(image_files)

        # Parse all extracted text
        all_text = [r.raw_text for r in results]
        parsed_data = parser_service.parse_multiple_texts(all_text)

        return ParsedOCRResponse(results=results, parsed_data=parsed_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OCR/Parse Error: {str(e)}")


@router.post("/api/pdf/fill")
async def fill_pdf_form(
    pdf_file: UploadFile = File(...),
    field_data: str = Form(...)
):
    """
    Fill a PDF form with the provided data.

    - **pdf_file**: The PDF form to fill
    - **field_data**: JSON string mapping field names to values
      Example: {"name": "John Doe", "date": "2024-01-15"}
    """
    validate_pdf(pdf_file)

    try:
        data = json.loads(field_data)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="field_data must be valid JSON")

    if not isinstance(data, dict):
        raise HTTPException(status_code=400, detail="field_data must be a JSON object")

    try:
        filled_pdf = pdf_service.fill_pdf(pdf_file.file, data)
        return Response(
            content=filled_pdf,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=filled_{pdf_file.filename}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error filling PDF: {str(e)}")


@router.post("/api/process")
async def process_complete(
    pdf_file: UploadFile = File(...),
    images: list[UploadFile] = File(...),
    field_mapping: str = Form(...)
):
    """
    Complete workflow: OCR images, map to fields, fill PDF.

    - **pdf_file**: The PDF form to fill
    - **images**: Images to extract text from (NID, passport, documents)
    - **field_mapping**: JSON mapping from PDF field names to data keys
      Example: {"pdf_name_field": "name", "pdf_date_field": "date"}

    The mapping tells which parsed data should fill which PDF field.
    Available data keys: names[0], dates[0], id_numbers[0], emails[0], phone_numbers[0], addresses[0]
    Or use "raw_text" to get all OCR text.
    """
    validate_pdf(pdf_file)
    for image in images:
        validate_image(image)

    try:
        mapping = json.loads(field_mapping)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="field_mapping must be valid JSON")

    try:
        # Step 1: OCR all images
        image_files = [(img.file, img.filename) for img in images]
        ocr_results = ocr_service.extract_from_multiple(image_files)

        # Step 2: Parse structured data
        all_text = [r.raw_text for r in ocr_results]
        parsed = parser_service.parse_multiple_texts(all_text)

        # Step 3: Build field data from mapping
        available_data = {
            "raw_text": "\n".join(all_text),
            "names": parsed.names,
            "dates": parsed.dates,
            "id_numbers": parsed.id_numbers,
            "addresses": parsed.addresses,
            "emails": parsed.emails,
            "phone_numbers": parsed.phone_numbers,
        }

        field_data = {}
        for pdf_field, data_key in mapping.items():
            # Handle indexed access like "names[0]"
            if "[" in data_key and "]" in data_key:
                key = data_key.split("[")[0]
                index = int(data_key.split("[")[1].split("]")[0])
                if key in available_data and isinstance(available_data[key], list):
                    if index < len(available_data[key]):
                        field_data[pdf_field] = available_data[key][index]
            elif data_key in available_data:
                value = available_data[data_key]
                field_data[pdf_field] = value if isinstance(value, str) else str(value)

        # Step 4: Fill the PDF
        pdf_file.file.seek(0)  # Reset file pointer
        filled_pdf = pdf_service.fill_pdf(pdf_file.file, field_data)

        return Response(
            content=filled_pdf,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename=filled_{pdf_file.filename}"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing Error: {str(e)}")
