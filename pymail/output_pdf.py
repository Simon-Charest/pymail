from fpdf import FPDF
from io import StringIO
from pathlib import Path
from typing import TextIO
import sys


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

    # Silence error handling
    original_stderr: TextIO = sys.stderr
    sys.stderr = StringIO()

    # Save the PDF
    pdf.output(path)

    # Restore error handling
    sys.stderr = original_stderr
