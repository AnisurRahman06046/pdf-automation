"""Test script for PDF Automation API."""
import requests
import json
import os

BASE_URL = "http://localhost:8000"
DEMO_DIR = "demo"


def test_health():
    """Test health endpoint."""
    print("\n" + "=" * 50)
    print("Testing: GET /health")
    print("=" * 50)

    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200


def test_pdf_fields():
    """Test PDF field extraction."""
    print("\n" + "=" * 50)
    print("Testing: POST /api/pdf/fields")
    print("=" * 50)

    pdf_path = f"{DEMO_DIR}/demo_form.pdf"
    if not os.path.exists(pdf_path):
        print(f"ERROR: {pdf_path} not found. Run generate_demo_pdf.py first.")
        return False

    with open(pdf_path, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/api/pdf/fields",
            files={"pdf_file": ("demo_form.pdf", f, "application/pdf")}
        )

    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Filename: {data['filename']}")
        print(f"Field count: {data['field_count']}")
        print("Fields:")
        for field in data["fields"]:
            print(f"  - {field['name']} ({field['field_type']})")
    else:
        print(f"Error: {response.text}")

    return response.status_code == 200


def test_ocr_extract():
    """Test OCR extraction."""
    print("\n" + "=" * 50)
    print("Testing: POST /api/ocr/extract")
    print("=" * 50)

    image_path = f"{DEMO_DIR}/demo_id_card.png"
    if not os.path.exists(image_path):
        print(f"ERROR: {image_path} not found. Run generate_demo_image.py first.")
        return False

    with open(image_path, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/api/ocr/extract",
            files={"images": ("demo_id_card.png", f, "image/png")}
        )

    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        for result in data["results"]:
            print(f"\nFile: {result['filename']}")
            print(f"Confidence: {result['confidence']}%")
            print(f"Extracted text:\n{result['raw_text'][:500]}...")
    else:
        print(f"Error: {response.text}")

    return response.status_code == 200


def test_ocr_parsed():
    """Test OCR with parsing."""
    print("\n" + "=" * 50)
    print("Testing: POST /api/ocr/extract-parsed")
    print("=" * 50)

    image_path = f"{DEMO_DIR}/demo_id_card.png"
    if not os.path.exists(image_path):
        print(f"ERROR: {image_path} not found.")
        return False

    with open(image_path, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/api/ocr/extract-parsed",
            files={"images": ("demo_id_card.png", f, "image/png")}
        )

    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        parsed = data["parsed_data"]
        print("\nParsed Data:")
        print(f"  Names: {parsed['names']}")
        print(f"  Dates: {parsed['dates']}")
        print(f"  ID Numbers: {parsed['id_numbers']}")
        print(f"  Emails: {parsed['emails']}")
        print(f"  Phones: {parsed['phone_numbers']}")
        print(f"  Addresses: {parsed['addresses']}")
    else:
        print(f"Error: {response.text}")

    return response.status_code == 200


def test_pdf_fill():
    """Test PDF filling."""
    print("\n" + "=" * 50)
    print("Testing: POST /api/pdf/fill")
    print("=" * 50)

    pdf_path = f"{DEMO_DIR}/demo_form.pdf"
    if not os.path.exists(pdf_path):
        print(f"ERROR: {pdf_path} not found.")
        return False

    field_data = {
        "full_name": "John Michael Smith",
        "dob": "15/03/1990",
        "id_number": "1234567890123",
        "email": "john.smith@email.com",
        "phone": "+1-555-123-4567",
        "address": "123 Main Street"
    }

    with open(pdf_path, "rb") as f:
        response = requests.post(
            f"{BASE_URL}/api/pdf/fill",
            files={"pdf_file": ("demo_form.pdf", f, "application/pdf")},
            data={"field_data": json.dumps(field_data)}
        )

    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        output_path = f"{DEMO_DIR}/filled_form.pdf"
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Filled PDF saved to: {output_path}")
    else:
        print(f"Error: {response.text}")

    return response.status_code == 200


def test_process_complete():
    """Test complete workflow."""
    print("\n" + "=" * 50)
    print("Testing: POST /api/process (Complete Workflow)")
    print("=" * 50)

    pdf_path = f"{DEMO_DIR}/demo_form.pdf"
    image_path = f"{DEMO_DIR}/demo_id_card.png"

    if not os.path.exists(pdf_path) or not os.path.exists(image_path):
        print("ERROR: Demo files not found.")
        return False

    # Map PDF fields to parsed data keys
    field_mapping = {
        "full_name": "names[0]",
        "dob": "dates[0]",
        "id_number": "id_numbers[0]",
        "email": "emails[0]",
        "phone": "phone_numbers[0]",
        "address": "addresses[0]"
    }

    with open(pdf_path, "rb") as pdf_file, open(image_path, "rb") as img_file:
        response = requests.post(
            f"{BASE_URL}/api/process",
            files=[
                ("pdf_file", ("demo_form.pdf", pdf_file, "application/pdf")),
                ("images", ("demo_id_card.png", img_file, "image/png"))
            ],
            data={"field_mapping": json.dumps(field_mapping)}
        )

    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        output_path = f"{DEMO_DIR}/auto_filled_form.pdf"
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Auto-filled PDF saved to: {output_path}")
    else:
        print(f"Error: {response.text}")

    return response.status_code == 200


def main():
    """Run all tests."""
    print("\n" + "#" * 60)
    print("  PDF AUTOMATION API - TEST SUITE")
    print("#" * 60)

    results = {
        "Health Check": test_health(),
        "PDF Fields": test_pdf_fields(),
        "OCR Extract": test_ocr_extract(),
        "OCR Parsed": test_ocr_parsed(),
        "PDF Fill": test_pdf_fill(),
        "Complete Process": test_process_complete(),
    }

    print("\n" + "=" * 50)
    print("TEST RESULTS SUMMARY")
    print("=" * 50)
    for test_name, passed in results.items():
        status = "PASS" if passed else "FAIL"
        print(f"  {test_name}: {status}")

    passed_count = sum(results.values())
    total_count = len(results)
    print(f"\nTotal: {passed_count}/{total_count} tests passed")


if __name__ == "__main__":
    main()
