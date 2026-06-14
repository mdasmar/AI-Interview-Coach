from pypdf import PdfReader


def extract_resume_text(uploaded_file):

    try:

        reader = PdfReader(
            uploaded_file
        )

        text = ""
        image_count = 0

        for page in reader.pages:

            page_text = (
                page.extract_text()
            )

            if page_text:

                text += (
                    page_text + "\n"
                )

            image_count += len(
                getattr(page, "images", [])
            )

        text = text.strip()

        if text:
            return text

        if image_count:
            return (
                "Error reading resume: This PDF appears to contain scanned "
                "images instead of selectable text. Please upload a text-based "
                "PDF or run OCR on the resume first."
            )

        return (
            "Error reading resume: No readable text was found in this PDF."
        )

    except Exception as e:

        return (
            f"Error reading resume: {str(e)}"
        )
