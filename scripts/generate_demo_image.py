"""Generate demo images with text for OCR testing."""
from PIL import Image, ImageDraw, ImageFont


def get_font(size, bold=False):
    """Get font, fallback to default if not available."""
    try:
        if bold:
            return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except OSError:
        return ImageFont.load_default()


def create_id_card_image():
    """Create a mock ID card image for OCR testing."""
    img = Image.new("RGB", (600, 400), color="white")
    draw = ImageDraw.Draw(img)

    font_large = get_font(24, bold=True)
    font_medium = get_font(18)
    font_small = get_font(14)

    # Border and header
    draw.rectangle([10, 10, 590, 390], outline="navy", width=3)
    draw.rectangle([10, 10, 590, 60], fill="navy")
    draw.text((180, 20), "NATIONAL ID CARD", fill="white", font=font_large)

    # Photo placeholder
    draw.rectangle([30, 80, 170, 250], outline="gray", width=2)
    draw.text((70, 155), "PHOTO", fill="gray", font=font_medium)

    # Personal information
    info_x = 200
    draw.text((info_x, 90), "Name: John Michael Smith", fill="black", font=font_medium)
    draw.text((info_x, 120), "Date of Birth: 15/03/1990", fill="black", font=font_medium)
    draw.text((info_x, 150), "Gender: Male", fill="black", font=font_medium)
    draw.text((info_x, 180), "ID Number: 1234567890123", fill="black", font=font_medium)
    draw.text((info_x, 210), "Nationality: American", fill="black", font=font_medium)
    draw.text((info_x, 240), "Blood Group: O+", fill="black", font=font_medium)

    # Address
    draw.text((30, 270), "Address: 123 Main Street, New York, NY 10001", fill="black", font=font_small)

    # Contact info
    draw.text((30, 300), "Email: john.smith@email.com", fill="black", font=font_small)
    draw.text((30, 325), "Phone: +1-555-123-4567", fill="black", font=font_small)

    # Father's name
    draw.text((30, 355), "Father's Name: Robert Smith", fill="black", font=font_small)

    output_path = "demo/demo_id_card.png"
    img.save(output_path)
    print(f"Created: {output_path}")


def create_passport_image():
    """Create a mock passport data page for OCR testing."""
    img = Image.new("RGB", (650, 450), color="white")
    draw = ImageDraw.Draw(img)

    font_large = get_font(20, bold=True)
    font_medium = get_font(16)
    font_mono = get_font(14)

    # Border
    draw.rectangle([5, 5, 645, 445], outline="darkgreen", width=4)

    # Header
    draw.text((250, 15), "PASSPORT", fill="darkgreen", font=font_large)
    draw.text((220, 45), "UNITED STATES OF AMERICA", fill="darkgreen", font=font_medium)

    # Photo placeholder
    draw.rectangle([25, 85, 175, 275], outline="gray", width=2)
    draw.text((70, 170), "PHOTO", fill="gray", font=font_medium)

    # Details
    info_x = 195
    details = [
        ("Type:", "P"),
        ("Country Code:", "USA"),
        ("Passport No.:", "AB1234567"),
        ("Surname:", "SMITH"),
        ("Given Names:", "JOHN MICHAEL"),
        ("Nationality:", "AMERICAN"),
        ("Date of Birth:", "15 Mar 1990"),
        ("Sex:", "M"),
        ("Place of Birth:", "NEW YORK"),
        ("Date of Issue:", "01 Jan 2020"),
        ("Date of Expiry:", "31 Dec 2030"),
    ]

    y = 85
    for label, value in details:
        draw.text((info_x, y), f"{label} {value}", fill="black", font=font_medium)
        y += 28

    # MRZ at bottom
    draw.rectangle([10, 385, 640, 440], fill="lightyellow")
    draw.text((15, 390), "P<USASMITH<<JOHN<MICHAEL<<<<<<<<<<<<<<<<<<<<<", fill="black", font=font_mono)
    draw.text((15, 415), "AB1234567<8USA9003150M3012319<<<<<<<<<<<<<<00", fill="black", font=font_mono)

    output_path = "demo/demo_passport.png"
    img.save(output_path)
    print(f"Created: {output_path}")


def create_comprehensive_document():
    """Create a comprehensive document with all fields for testing."""
    img = Image.new("RGB", (800, 1000), color="white")
    draw = ImageDraw.Draw(img)

    font_title = get_font(22, bold=True)
    font_section = get_font(16, bold=True)
    font_normal = get_font(14)

    # Title
    draw.rectangle([0, 0, 800, 50], fill="darkblue")
    draw.text((250, 12), "PERSONAL INFORMATION DOCUMENT", fill="white", font=font_title)

    y = 70

    # Personal Information
    draw.text((30, y), "PERSONAL DETAILS", fill="darkblue", font=font_section)
    y += 30
    personal_info = [
        "First Name: John",
        "Middle Name: Michael",
        "Last Name: Smith",
        "Date of Birth: 15/03/1990",
        "Age: 34",
        "Gender: Male",
        "Nationality: American",
        "Marital Status: Married",
        "Father's Name: Robert James Smith",
        "Mother's Name: Mary Elizabeth Smith",
        "Spouse Name: Sarah Johnson Smith",
        "Place of Birth: New York City",
        "Blood Group: O+",
    ]
    for info in personal_info:
        draw.text((50, y), info, fill="black", font=font_normal)
        y += 22

    y += 15

    # Contact Information
    draw.text((30, y), "CONTACT INFORMATION", fill="darkblue", font=font_section)
    y += 30
    contact_info = [
        "Email: john.smith@email.com",
        "Phone Number: +1-555-123-4567",
        "Alternate Phone: +1-555-987-6543",
        "Permanent Address: 123 Main Street, Apt 4B",
        "City: New York",
        "State: New York",
        "Postal Code: 10001",
        "Country: United States",
        "Current Address: 456 Oak Avenue, Suite 12",
    ]
    for info in contact_info:
        draw.text((50, y), info, fill="black", font=font_normal)
        y += 22

    y += 15

    # Identification
    draw.text((30, y), "IDENTIFICATION DOCUMENTS", fill="darkblue", font=font_section)
    y += 30
    id_info = [
        "National ID Number: 1234567890123",
        "Passport Number: AB1234567",
        "Driver License: DL98765432",
        "Tax ID (SSN): 123-45-6789",
        "Voter ID: VTR2024NYC001",
    ]
    for info in id_info:
        draw.text((50, y), info, fill="black", font=font_normal)
        y += 22

    y += 15

    # Employment
    draw.text((30, y), "EMPLOYMENT & EDUCATION", fill="darkblue", font=font_section)
    y += 30
    emp_info = [
        "Occupation: Software Engineer",
        "Job Title: Senior Developer",
        "Employer Name: Tech Solutions Inc.",
        "Work Address: 789 Corporate Blvd, Tech Park",
        "Years of Experience: 10",
        "Highest Qualification: Master's Degree",
        "Institution Name: MIT",
        "Year of Passing: 2015",
    ]
    for info in emp_info:
        draw.text((50, y), info, fill="black", font=font_normal)
        y += 22

    y += 15

    # Financial
    draw.text((30, y), "FINANCIAL INFORMATION", fill="darkblue", font=font_section)
    y += 30
    fin_info = [
        "Bank Account Number: 9876543210",
        "Bank Name: National Bank of America",
        "Branch: Manhattan Downtown",
        "Annual Income: 150000",
    ]
    for info in fin_info:
        draw.text((50, y), info, fill="black", font=font_normal)
        y += 22

    y += 15

    # Emergency Contact
    draw.text((30, y), "EMERGENCY CONTACT", fill="darkblue", font=font_section)
    y += 30
    emergency_info = [
        "Emergency Contact Name: Robert Smith",
        "Relationship: Father",
        "Emergency Phone: +1-555-111-2222",
    ]
    for info in emergency_info:
        draw.text((50, y), info, fill="black", font=font_normal)
        y += 22

    output_path = "demo/comprehensive_document.png"
    img.save(output_path)
    print(f"Created: {output_path}")


def create_italian_document():
    """Create an Italian document for testing."""
    img = Image.new("RGB", (700, 600), color="white")
    draw = ImageDraw.Draw(img)

    font_title = get_font(20, bold=True)
    font_section = get_font(14, bold=True)
    font_normal = get_font(13)

    # Title
    draw.rectangle([0, 0, 700, 45], fill="green")
    draw.text((200, 10), "DOCUMENTO D'IDENTITA", fill="white", font=font_title)

    y = 60

    # Personal Info
    draw.text((30, y), "DATI PERSONALI", fill="green", font=font_section)
    y += 25
    info = [
        "Nome: Marco",
        "Cognome: Rossi",
        "Data di Nascita: 20/05/1985",
        "Luogo di Nascita: Roma",
        "Sesso: Maschio",
        "Stato Civile: Coniugato",
        "Nazionalita: Italiana",
        "Codice Fiscale: RSSMRC85E20H501X",
    ]
    for line in info:
        draw.text((50, y), line, fill="black", font=font_normal)
        y += 22

    y += 10

    # Contact
    draw.text((30, y), "CONTATTI", fill="green", font=font_section)
    y += 25
    contact = [
        "Indirizzo Residenza: Via Roma 123",
        "Citta: Milano",
        "Provincia: MI",
        "CAP: 20100",
        "Telefono: +39-02-1234567",
        "Cellulare: +39-333-1234567",
        "Email: marco.rossi@email.it",
    ]
    for line in contact:
        draw.text((50, y), line, fill="black", font=font_normal)
        y += 22

    y += 10

    # Work
    draw.text((30, y), "LAVORO", fill="green", font=font_section)
    y += 25
    work = [
        "Professione: Ingegnere",
        "Datore di Lavoro: Fiat SpA",
    ]
    for line in work:
        draw.text((50, y), line, fill="black", font=font_normal)
        y += 22

    output_path = "demo/italian_document.png"
    img.save(output_path)
    print(f"Created: {output_path}")


if __name__ == "__main__":
    import os
    os.makedirs("demo", exist_ok=True)
    create_id_card_image()
    create_passport_image()
    create_comprehensive_document()
    create_italian_document()
    print("\nAll images created successfully!")
