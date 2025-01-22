from megaparse import MegaParse
import os
import re

def clean_text(text: str) -> str:
    """Clean and normalize the extracted text"""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters but keep basic punctuation 
    text = re.sub(r'[^\w\s.,;()-@]', '', text)
    # Normalize line breaks
    text = text.replace('\n', ' ').strip()
    return text

# PDF file path
pdf_path = r"C:\Users\isult\OneDrive\Documents\CV_extract\CVs\cv_leads\64478-Mohammad-Samer-Mohammad-Alkhammash.pdf"

try:
    print(f"Extracting text from: {pdf_path}")
    # Extract text using MegaParse
    megaparse = MegaParse(pdf_path)
    text = str(megaparse.load())  # Convert to string before processing

    if not text.strip():
        print("Warning: No text extracted from PDF")
    else:
        # Clean the extracted text
        cleaned_text = clean_text(text)
        print("\nExtracted and cleaned text:")
        print("-" * 50)
        print(cleaned_text)
        print("-" * 50)
        print("\nText extraction completed successfully")

except Exception as e:
    print(f"Error processing PDF: {str(e)}")
