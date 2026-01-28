"""Generate a demo fillable PDF form for testing."""
import fitz


def create_demo_pdf():
    """Create a simple fillable PDF form."""
    doc = fitz.open()
    page = doc.new_page(width=595, height=842)  # A4 size

    # Title
    page.insert_text((200, 50), "Application Form", fontsize=20, fontname="helv")

    # Add form fields with labels
    fields = [
        ("Full Name:", "full_name", 100),
        ("Date of Birth:", "dob", 150),
        ("ID Number:", "id_number", 200),
        ("Email:", "email", 250),
        ("Phone:", "phone", 300),
        ("Address:", "address", 350),
    ]

    for label, field_name, y_pos in fields:
        # Label
        page.insert_text((50, y_pos), label, fontsize=12, fontname="helv")

        # Text field widget
        widget = fitz.Widget()
        widget.field_type = fitz.PDF_WIDGET_TYPE_TEXT
        widget.field_name = field_name
        widget.rect = fitz.Rect(150, y_pos - 15, 400, y_pos + 5)
        widget.field_value = ""
        widget.text_fontsize = 11
        widget.border_color = (0, 0, 0)
        widget.fill_color = (0.95, 0.95, 0.95)
        page.add_widget(widget)

    # Save the PDF
    output_path = "demo/demo_form.pdf"
    doc.save(output_path)
    doc.close()
    print(f"Created: {output_path}")
    return output_path


if __name__ == "__main__":
    import os
    os.makedirs("demo", exist_ok=True)
    create_demo_pdf()
