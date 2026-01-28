"""Generate demo fillable PDF forms for testing."""
import fitz


def create_demo_pdf():
    """Create a simple fillable PDF form."""
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)

    page.insert_text((200, 50), "Application Form", fontsize=20, fontname="helv")

    fields = [
        ("Full Name:", "full_name", 100),
        ("Date of Birth:", "dob", 150),
        ("ID Number:", "id_number", 200),
        ("Email:", "email", 250),
        ("Phone:", "phone", 300),
        ("Address:", "address", 350),
    ]

    for label, field_name, y_pos in fields:
        page.insert_text((50, y_pos), label, fontsize=12, fontname="helv")
        widget = fitz.Widget()
        widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        widget.field_name = field_name
        widget.rect = fitz.Rect(150, y_pos - 15, 400, y_pos + 5)
        widget.field_value = ""
        widget.text_fontsize = 11
        widget.border_color = (0, 0, 0)
        widget.fill_color = (0.95, 0.95, 0.95)
        page.add_widget(widget)

    output_path = "demo/demo_form.pdf"
    doc.save(output_path)
    doc.close()
    print(f"Created: {output_path}")


def create_comprehensive_form():
    """Create a comprehensive form with worldwide fields."""
    doc = fitz.open()

    # Page 1 - Personal Information
    page1 = doc.new_page(width=595, height=842)
    page1.insert_text((180, 40), "COMPREHENSIVE APPLICATION FORM", fontsize=16, fontname="helv")
    page1.insert_text((50, 70), "Section 1: Personal Information", fontsize=12, fontname="helv")

    fields_page1 = [
        ("First Name:", "first_name", 100),
        ("Middle Name:", "middle_name", 130),
        ("Last Name:", "last_name", 160),
        ("Date of Birth:", "date_of_birth", 190),
        ("Age:", "age", 220),
        ("Gender:", "gender", 250),
        ("Nationality:", "nationality", 280),
        ("Marital Status:", "marital_status", 310),
        ("Father's Name:", "father_name", 340),
        ("Mother's Name:", "mother_name", 370),
        ("Spouse Name:", "spouse_name", 400),
        ("Place of Birth:", "place_of_birth", 430),
        ("Blood Group:", "blood_group", 460),
    ]

    for label, field_name, y_pos in fields_page1:
        page1.insert_text((50, y_pos), label, fontsize=10, fontname="helv")
        widget = fitz.Widget()
        widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        widget.field_name = field_name
        widget.rect = fitz.Rect(170, y_pos - 12, 400, y_pos + 5)
        widget.text_fontsize = 10
        widget.border_color = (0, 0, 0)
        widget.fill_color = (0.97, 0.97, 0.97)
        page1.add_widget(widget)

    # Section 2 - Contact Information (same page)
    page1.insert_text((50, 500), "Section 2: Contact Information", fontsize=12, fontname="helv")

    fields_contact = [
        ("Email:", "email", 530),
        ("Phone Number:", "phone_number", 560),
        ("Alternate Phone:", "alternate_phone_number", 590),
        ("Permanent Address:", "permanent_address", 620),
        ("City:", "city", 650),
        ("State/Province:", "state", 680),
        ("Postal Code:", "postal_code", 710),
        ("Country:", "country", 740),
        ("Current Address:", "current_address", 770),
    ]

    for label, field_name, y_pos in fields_contact:
        page1.insert_text((50, y_pos), label, fontsize=10, fontname="helv")
        widget = fitz.Widget()
        widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        widget.field_name = field_name
        widget.rect = fitz.Rect(170, y_pos - 12, 550, y_pos + 5)
        widget.text_fontsize = 10
        widget.border_color = (0, 0, 0)
        widget.fill_color = (0.97, 0.97, 0.97)
        page1.add_widget(widget)

    # Page 2 - IDs, Employment, Financial
    page2 = doc.new_page(width=595, height=842)
    page2.insert_text((50, 40), "Section 3: Identification Documents", fontsize=12, fontname="helv")

    fields_ids = [
        ("National ID Number:", "national_id_number", 70),
        ("Passport Number:", "passport_number", 100),
        ("Driver License:", "driver_license_number", 130),
        ("Tax ID (SSN/PAN):", "tax_id", 160),
        ("Voter ID:", "voter_id", 190),
    ]

    for label, field_name, y_pos in fields_ids:
        page2.insert_text((50, y_pos), label, fontsize=10, fontname="helv")
        widget = fitz.Widget()
        widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        widget.field_name = field_name
        widget.rect = fitz.Rect(180, y_pos - 12, 400, y_pos + 5)
        widget.text_fontsize = 10
        widget.border_color = (0, 0, 0)
        widget.fill_color = (0.97, 0.97, 0.97)
        page2.add_widget(widget)

    # Employment
    page2.insert_text((50, 240), "Section 4: Employment & Education", fontsize=12, fontname="helv")

    fields_emp = [
        ("Occupation:", "occupation", 270),
        ("Job Title:", "job_title", 300),
        ("Employer Name:", "employer_name", 330),
        ("Work Address:", "work_address", 360),
        ("Years of Experience:", "years_of_experience", 390),
        ("Highest Qualification:", "highest_qualification", 420),
        ("Institution Name:", "institution_name", 450),
        ("Year of Passing:", "year_of_passing", 480),
    ]

    for label, field_name, y_pos in fields_emp:
        page2.insert_text((50, y_pos), label, fontsize=10, fontname="helv")
        widget = fitz.Widget()
        widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        widget.field_name = field_name
        widget.rect = fitz.Rect(180, y_pos - 12, 500, y_pos + 5)
        widget.text_fontsize = 10
        widget.border_color = (0, 0, 0)
        widget.fill_color = (0.97, 0.97, 0.97)
        page2.add_widget(widget)

    # Financial
    page2.insert_text((50, 530), "Section 5: Financial Information", fontsize=12, fontname="helv")

    fields_fin = [
        ("Bank Account Number:", "bank_account_number", 560),
        ("Bank Name:", "bank_name", 590),
        ("Branch:", "branch", 620),
        ("Annual Income:", "income", 650),
    ]

    for label, field_name, y_pos in fields_fin:
        page2.insert_text((50, y_pos), label, fontsize=10, fontname="helv")
        widget = fitz.Widget()
        widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        widget.field_name = field_name
        widget.rect = fitz.Rect(180, y_pos - 12, 400, y_pos + 5)
        widget.text_fontsize = 10
        widget.border_color = (0, 0, 0)
        widget.fill_color = (0.97, 0.97, 0.97)
        page2.add_widget(widget)

    # Emergency Contact
    page2.insert_text((50, 700), "Section 6: Emergency Contact", fontsize=12, fontname="helv")

    fields_emergency = [
        ("Emergency Contact Name:", "emergency_contact_name", 730),
        ("Relationship:", "relationship", 760),
        ("Emergency Phone:", "emergency_contact_phone", 790),
    ]

    for label, field_name, y_pos in fields_emergency:
        page2.insert_text((50, y_pos), label, fontsize=10, fontname="helv")
        widget = fitz.Widget()
        widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        widget.field_name = field_name
        widget.rect = fitz.Rect(200, y_pos - 12, 450, y_pos + 5)
        widget.text_fontsize = 10
        widget.border_color = (0, 0, 0)
        widget.fill_color = (0.97, 0.97, 0.97)
        page2.add_widget(widget)

    output_path = "demo/comprehensive_form.pdf"
    doc.save(output_path)
    doc.close()
    print(f"Created: {output_path}")


def create_italian_form():
    """Create an Italian form."""
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)

    page.insert_text((200, 40), "MODULO DI DOMANDA", fontsize=18, fontname="helv")
    page.insert_text((50, 70), "Informazioni Personali", fontsize=12, fontname="helv")

    fields = [
        ("Nome:", "nome", 100),
        ("Cognome:", "cognome", 130),
        ("Data di Nascita:", "data_nascita", 160),
        ("Luogo di Nascita:", "luogo_nascita", 190),
        ("Sesso:", "sesso", 220),
        ("Stato Civile:", "stato_civile", 250),
        ("Nazionalità:", "nazionalita", 280),
        ("Codice Fiscale:", "codice_fiscale", 310),
        ("Indirizzo Residenza:", "indirizzo_residenza", 340),
        ("Città:", "citta", 370),
        ("Provincia:", "provincia", 400),
        ("CAP:", "cap", 430),
        ("Telefono:", "telefono", 460),
        ("Cellulare:", "cellulare", 490),
        ("Email:", "email", 520),
        ("Professione:", "professione", 550),
        ("Datore di Lavoro:", "datore_lavoro", 580),
    ]

    for label, field_name, y_pos in fields:
        page.insert_text((50, y_pos), label, fontsize=10, fontname="helv")
        widget = fitz.Widget()
        widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        widget.field_name = field_name
        widget.rect = fitz.Rect(180, y_pos - 12, 450, y_pos + 5)
        widget.text_fontsize = 10
        widget.border_color = (0, 0, 0)
        widget.fill_color = (0.97, 0.97, 0.97)
        page.add_widget(widget)

    output_path = "demo/italian_form.pdf"
    doc.save(output_path)
    doc.close()
    print(f"Created: {output_path}")


if __name__ == "__main__":
    import os
    os.makedirs("demo", exist_ok=True)
    create_demo_pdf()
    create_comprehensive_form()
    create_italian_form()
    print("\nAll forms created successfully!")
