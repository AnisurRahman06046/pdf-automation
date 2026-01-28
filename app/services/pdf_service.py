import fitz
from pathlib import Path
from typing import BinaryIO

from app.models.schemas import PDFField


def get_form_fields(pdf_file: BinaryIO) -> list[PDFField]:
    """Extract all form fields from a PDF."""
    pdf_bytes = pdf_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    fields = []
    for page in doc:
        widgets = page.widgets()
        if widgets:
            for widget in widgets:
                field_type_map = {
                    fitz.PDF_WIDGET_TYPE_TEXT: "text",
                    fitz.PDF_WIDGET_TYPE_CHECKBOX: "checkbox",
                    fitz.PDF_WIDGET_TYPE_RADIOBUTTON: "radio",
                    fitz.PDF_WIDGET_TYPE_LISTBOX: "listbox",
                    fitz.PDF_WIDGET_TYPE_COMBOBOX: "combobox",
                    fitz.PDF_WIDGET_TYPE_SIGNATURE: "signature",
                }

                field = PDFField(
                    name=widget.field_name or f"unnamed_field_{len(fields)}",
                    field_type=field_type_map.get(widget.field_type, "unknown"),
                    value=widget.field_value
                )
                fields.append(field)

    doc.close()
    return fields


def fill_pdf(pdf_file: BinaryIO, field_data: dict[str, str]) -> bytes:
    """Fill a PDF form with the provided field data."""
    pdf_bytes = pdf_file.read()
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    for page in doc:
        widgets = page.widgets()
        if widgets:
            for widget in widgets:
                field_name = widget.field_name
                if field_name and field_name in field_data:
                    widget.field_value = field_data[field_name]
                    widget.update()

    output_bytes = doc.tobytes()
    doc.close()
    return output_bytes


def get_field_names(pdf_file: BinaryIO) -> list[str]:
    """Get just the field names from a PDF."""
    fields = get_form_fields(pdf_file)
    return [f.name for f in fields]
