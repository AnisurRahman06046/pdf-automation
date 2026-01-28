import re
from app.models.schemas import ParsedData


def extract_names(text: str) -> list[str]:
    """Extract potential names from text."""
    # Pattern for names: capitalized words that appear together
    # Matches patterns like "John Doe", "Mary Jane Smith"
    name_pattern = r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\b"
    matches = re.findall(name_pattern, text)
    return list(set(matches))


def extract_dates(text: str) -> list[str]:
    """Extract dates in various formats."""
    patterns = [
        r"\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b",  # DD/MM/YYYY or MM-DD-YY
        r"\b(\d{4}[/-]\d{1,2}[/-]\d{1,2})\b",  # YYYY-MM-DD
        r"\b(\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4})\b",  # 12 Jan 2024
        r"\b((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},?\s+\d{2,4})\b",  # Jan 12, 2024
    ]

    dates = []
    for pattern in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        dates.extend(matches)

    return list(set(dates))


def extract_id_numbers(text: str) -> list[str]:
    """Extract potential ID numbers (passport, NID, etc.)."""
    patterns = [
        r"\b([A-Z]{1,2}\d{6,9})\b",  # Passport-like: AB1234567
        r"\b(\d{9,17})\b",  # Long numeric IDs (NID, SSN, etc.)
        r"\b(\d{3}[-\s]?\d{2}[-\s]?\d{4})\b",  # SSN format: 123-45-6789
    ]

    ids = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        ids.extend(matches)

    return list(set(ids))


def extract_addresses(text: str) -> list[str]:
    """Extract potential addresses from text."""
    # Pattern for street addresses
    address_pattern = r"\b(\d+\s+[A-Za-z]+(?:\s+[A-Za-z]+)*(?:\s+(?:Street|St|Avenue|Ave|Road|Rd|Drive|Dr|Lane|Ln|Boulevard|Blvd|Way|Court|Ct|Place|Pl))\.?(?:,?\s*(?:Apt|Suite|Unit|#)\.?\s*\d+)?)\b"
    matches = re.findall(address_pattern, text, re.IGNORECASE)
    return list(set(matches))


def extract_emails(text: str) -> list[str]:
    """Extract email addresses."""
    email_pattern = r"\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b"
    matches = re.findall(email_pattern, text)
    return list(set(matches))


def extract_phone_numbers(text: str) -> list[str]:
    """Extract phone numbers in various formats."""
    patterns = [
        r"\b(\+?\d{1,3}[-.\s]?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4})\b",  # International
        r"\b(\(\d{3}\)\s*\d{3}[-.\s]?\d{4})\b",  # (123) 456-7890
        r"\b(\d{3}[-.\s]\d{3}[-.\s]\d{4})\b",  # 123-456-7890
    ]

    phones = []
    for pattern in patterns:
        matches = re.findall(pattern, text)
        phones.extend(matches)

    return list(set(phones))


def parse_text(text: str) -> ParsedData:
    """Parse text and extract structured data."""
    return ParsedData(
        names=extract_names(text),
        dates=extract_dates(text),
        id_numbers=extract_id_numbers(text),
        addresses=extract_addresses(text),
        emails=extract_emails(text),
        phone_numbers=extract_phone_numbers(text)
    )


def parse_multiple_texts(texts: list[str]) -> ParsedData:
    """Parse multiple texts and combine results."""
    combined_text = "\n".join(texts)
    return parse_text(combined_text)
