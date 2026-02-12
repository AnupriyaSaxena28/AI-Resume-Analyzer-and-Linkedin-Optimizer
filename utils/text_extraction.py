"""
Text Extraction Module
Extracts clean, readable text from PDF and DOCX files
"""

import PyPDF2
from docx import Document
import re


def extract_from_pdf(file):
    """
    Extract text from PDF file
    
    Args:
        file: Uploaded file object
        
    Returns:
        str: Extracted text
    """
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        
        for page in pdf_reader.pages:
            text += page.extract_text()
            
        return text
    except Exception as e:
        raise Exception(f"Error extracting PDF: {str(e)}")


def extract_from_docx(file):
    """
    Extract text from DOCX file
    
    Args:
        file: Uploaded file object
        
    Returns:
        str: Extracted text
    """
    try:
        doc = Document(file)
        text = ""
        
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
            
        return text
    except Exception as e:
        raise Exception(f"Error extracting DOCX: {str(e)}")


def clean_text(text):
    """
    Clean and normalize extracted text
    
    Args:
        text: Raw extracted text
        
    Returns:
        str: Cleaned text
    """
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters but keep basic punctuation
    text = re.sub(r'[^\w\s\.\,\-\(\)\:\;\@]', '', text)
    
    # Normalize line breaks
    text = text.strip()
    
    return text


def extract_text(file, file_type):
    """
    Main extraction function that handles both PDF and DOCX
    
    Args:
        file: Uploaded file object
        file_type: Type of file ('pdf' or 'docx')
        
    Returns:
        str: Cleaned extracted text
    """
    try:
        if file_type.lower() == 'pdf':
            text = extract_from_pdf(file)
        elif file_type.lower() in ['docx', 'doc']:
            text = extract_from_docx(file)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
        # Clean the extracted text
        cleaned_text = clean_text(text)
        
        if not cleaned_text or len(cleaned_text) < 50:
            raise ValueError("Extracted text is too short or empty. Please check your file.")
        
        return cleaned_text
        
    except Exception as e:
        raise Exception(f"Text extraction failed: {str(e)}")


def get_word_count(text):
    """
    Get word count from text
    
    Args:
        text: Input text
        
    Returns:
        int: Word count
    """
    return len(text.split())


def estimate_reading_time(text):
    """
    Estimate reading time for text (assuming 200 words per minute)
    
    Args:
        text: Input text
        
    Returns:
        int: Estimated reading time in minutes
    """
    word_count = get_word_count(text)
    return max(1, word_count // 200)
