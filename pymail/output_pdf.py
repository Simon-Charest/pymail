from fpdf import FPDF


def output_pdf(text: str, path: str, family: str = "Arial", size: int = 12, width: float = 0, height: float = 10) -> None:
    pdf: FPDF = FPDF()  # Create instance of FPDF class
    pdf.add_page()  # Add a page
    pdf.set_font(family, size = size)  # Set font for the text
    pdf.multi_cell(width, height, text.encode('latin-1', 'replace').decode('latin-1'))  # Encode and decode using 'latin-1'
    pdf.output(path)  # Save the PDF
