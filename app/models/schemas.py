from pydantic import BaseModel
from typing import Optional


class HealthResponse(BaseModel):
    status: str
    message: str


class PDFField(BaseModel):
    name: str
    field_type: str
    value: Optional[str] = None


class PDFFieldsResponse(BaseModel):
    filename: str
    field_count: int
    fields: list[PDFField]


class ExtractedText(BaseModel):
    filename: str
    raw_text: str
    confidence: Optional[float] = None


class OCRResponse(BaseModel):
    results: list[ExtractedText]


class ParsedData(BaseModel):
    names: list[str]
    dates: list[str]
    id_numbers: list[str]
    addresses: list[str]
    emails: list[str]
    phone_numbers: list[str]


class ParsedOCRResponse(BaseModel):
    results: list[ExtractedText]
    parsed_data: ParsedData


class FillRequest(BaseModel):
    field_data: dict[str, str]


class ProcessRequest(BaseModel):
    field_mapping: dict[str, str]
