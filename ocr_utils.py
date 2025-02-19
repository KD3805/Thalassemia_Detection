# File: ocr_utils.py
import os
import cv2
import pytesseract
import tempfile
from PyPDF2 import PdfReader, errors as pdf_errors
from parse_blood_report import parse_blood_report  # Ensure this file is in the correct path

def extract_text_from_image(file_path: str) -> str:
    """
    Extract text from an image file using pytesseract.
    """
    image = cv2.imread(file_path)
    if image is None:
        raise ValueError("Unable to read the image file.")
    # Convert to grayscale for improved OCR accuracy.
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray, lang="eng")
    return text

def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from a PDF file using PyPDF2.
    """
    text = ""
    try:
        with open(file_path, 'rb') as f:
            reader = PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except pdf_errors.PdfReadError as e:
        raise ValueError(f"Error reading PDF file: {e}")
    return text

def extract_text_from_file(file_path: str, file_type: str = "image") -> str:
    """
    Extract text from a file based on its type.
    Supported types: "pdf", "jpg", "jpeg", "png"
    """
    if file_type.lower() == "pdf":
        return extract_text_from_pdf(file_path)
    elif file_type.lower() in ["jpg", "jpeg", "png"]:
        return extract_text_from_image(file_path)
    else:
        raise ValueError("Unsupported file type for text extraction.")

def extract_parameters_from_file(file_path: str, file_type: str = "image") -> dict:
    """
    Extracts text from the file and parses it to extract blood report parameters.
    This function integrates PDF and image extraction methods along with
    regex parsing (provided by parse_blood_report.py).
    """
    text = extract_text_from_file(file_path, file_type)
    parameters = parse_blood_report(text)
    return parameters

# For testing purposes:
if __name__ == "__main__":
    # Example usage for an image file:
    image_path = "example_report.jpg"  # Replace with an actual file path
    try:
        params = extract_parameters_from_file(image_path, "image")
        print("Extracted parameters from image:", params)
    except Exception as e:
        print("Error:", e)
    
    # Example usage for a PDF file:
    pdf_path = "example_report.pdf"  # Replace with an actual file path
    try:
        params = extract_parameters_from_file(pdf_path, "pdf")
        print("Extracted parameters from PDF:", params)
    except Exception as e:
        print("Error:", e)
