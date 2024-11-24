#!/usr/bin/env python3

import sys
import pymupdf
from pymupdf.utils import get_pixmap
from PIL import Image

def convert_pdf_to_png(pdf_path: str, page_number: int, output_path: str):
    try:
        doc = pymupdf.open(pdf_path)
    except FileNotFoundError:
        print(f"Error: File '{pdf_path}' not found.")
        sys.exit(-1)
    except Exception as e:
        print(f"Error opening PDF file: {str(e)}")
        sys.exit(-1)

    # Check if the PDF has enough pages
    if doc.page_count < page_number:
        print(f"Error: PDF file '{pdf_path}' has less than {page_number} pages.")
        doc.close()
        sys.exit(-1)

    # Get the page and convert it to a pixmap with 600 DPI
    page = doc[page_number-1]

    # zoom = 600 / 72  # Convert DPI to zoom factor
    # mat = pymupdf.Matrix(zoom, zoom)
    # pix = page.get_pixmap(matrix=mat)

    pix = get_pixmap(page=page, dpi=600)

    # Convert pixmap to Pillow Image
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)

    # Resize the image to 900px wide
    img = img.resize((900, int(img.height * 900 / img.width)))

    doc.close()

    # Save the resized image
    try:
        img.save(output_path, "PNG")
    except Exception as e:
        print(f"Error saving PNG file: {str(e)}")
        sys.exit(-1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script_name.py <input_pdf> <page_number> <output_png>")
        sys.exit(-1)
    else:
        convert_pdf_to_png(sys.argv[1], int(sys.argv[2]), sys.argv[3])
