from fpdf import FPDF
from pathlib import Path


def output_pdf(
    text: str,
    path: Path,
    family: str = None,
    fname: Path = None,
    size: int = 12,
    width: float = 0,
    height: float = 10
) -> None:
    # Create instance of FPDF class
    pdf: FPDF = FPDF()
    
    # Add a page
    pdf.add_page()

    if fname:
        family = fname.stem
        pdf.add_font(family, fname=fname)

    if family:
         # Set font for the text
        pdf.set_font(family, size=size)
    
    pdf.multi_cell(width, height, text)

    # Save the PDF
    pdf.output(path)
