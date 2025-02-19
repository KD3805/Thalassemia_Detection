import requests
import PyPDF2
import os

def extract_text_from_pdf(url, temp_filename='temp.pdf'):
    response = requests.get(url)
    response.raise_for_status()

    with open(temp_filename, 'wb') as temp_file:
        temp_file.write(response.content)

    text = ''
    try:
        with open(temp_filename, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
    except PyPDF2.errors.PdfReadError as e:
        print(f"PDF read error: {e}")

    os.remove(temp_filename)

    return text