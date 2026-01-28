"""Generate demo images with text for OCR testing."""
from PIL import Image, ImageDraw, ImageFont


def create_id_card_image():
    """Create a mock ID card image for OCR testing."""
    # Create image with white background
    img = Image.new("RGB", (600, 400), color="white")
    draw = ImageDraw.Draw(img)

    # Try to use a basic font, fall back to default if not available
    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
    except OSError:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw border
    draw.rectangle([10, 10, 590, 390], outline="navy", width=3)

    # Header
    draw.rectangle([10, 10, 590, 60], fill="navy")
    draw.text((180, 20), "NATIONAL ID CARD", fill="white", font=font_large)

    # Photo placeholder
    draw.rectangle([30, 80, 170, 250], outline="gray", width=2)
    draw.text((70, 155), "PHOTO", fill="gray", font=font_medium)

    # Personal information
    info_x = 200
    draw.text((info_x, 90), "Name:", fill="gray", font=font_small)
    draw.text((info_x, 110), "John Michael Smith", fill="black", font=font_medium)

    draw.text((info_x, 150), "Date of Birth:", fill="gray", font=font_small)
    draw.text((info_x, 170), "15/03/1990", fill="black", font=font_medium)

    draw.text((info_x, 210), "ID Number:", fill="gray", font=font_small)
    draw.text((info_x, 230), "1234567890123", fill="black", font=font_medium)

    draw.text((info_x, 270), "Address:", fill="gray", font=font_small)
    draw.text((info_x, 290), "123 Main Street", fill="black", font=font_medium)

    # Contact info at bottom
    draw.text((30, 320), "Email: john.smith@email.com", fill="black", font=font_small)
    draw.text((30, 345), "Phone: +1-555-123-4567", fill="black", font=font_small)

    # Save
    output_path = "demo/demo_id_card.png"
    img.save(output_path)
    print(f"Created: {output_path}")
    return output_path


def create_passport_image():
    """Create a mock passport data page for OCR testing."""
    img = Image.new("RGB", (600, 420), color="white")
    draw = ImageDraw.Draw(img)

    try:
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        font_medium = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
        font_mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14)
    except OSError:
        font_large = ImageFont.load_default()
        font_medium = ImageFont.load_default()
        font_mono = ImageFont.load_default()

    # Border
    draw.rectangle([5, 5, 595, 415], outline="darkgreen", width=4)

    # Header
    draw.text((200, 20), "PASSPORT", fill="darkgreen", font=font_large)
    draw.text((220, 50), "BANGLADESH", fill="darkgreen", font=font_medium)

    # Photo placeholder
    draw.rectangle([30, 90, 180, 280], outline="gray", width=2)
    draw.text((75, 175), "PHOTO", fill="gray", font=font_medium)

    # Details
    info_x = 200
    details = [
        ("Type", "P"),
        ("Country Code", "BGD"),
        ("Passport No.", "AB1234567"),
        ("Surname", "RAHMAN"),
        ("Given Names", "MOHAMMAD KARIM"),
        ("Nationality", "BANGLADESHI"),
        ("Date of Birth", "25 Dec 1985"),
        ("Sex", "M"),
        ("Place of Birth", "DHAKA"),
        ("Date of Issue", "01 Jan 2020"),
        ("Date of Expiry", "31 Dec 2030"),
    ]

    y = 90
    for label, value in details:
        draw.text((info_x, y), f"{label}:", fill="gray", font=font_mono)
        draw.text((info_x + 150, y), value, fill="black", font=font_medium)
        y += 25

    # MRZ at bottom
    draw.rectangle([10, 360, 590, 410], fill="lightyellow")
    draw.text((20, 365), "P<BGDRAHMAN<<MOHAMMAD<KARIM<<<<<<<<<<<<<<<<<<", fill="black", font=font_mono)
    draw.text((20, 385), "AB1234567<8BGD8512250M3012319<<<<<<<<<<<<<<00", fill="black", font=font_mono)

    output_path = "demo/demo_passport.png"
    img.save(output_path)
    print(f"Created: {output_path}")
    return output_path


if __name__ == "__main__":
    import os
    os.makedirs("demo", exist_ok=True)
    create_id_card_image()
    create_passport_image()
