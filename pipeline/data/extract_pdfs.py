#!/usr/bin/env python3
"""
PDF Text Extraction Script

This script extracts text from all PDF files in the pdfs/ directory
and saves them as .txt files with the same name in the same directory.

Requirements:
    pip install PyPDF2

Usage:
    python extract_pdfs.py
"""

import os
from pathlib import Path
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        Extracted text as a string
    """
    try:
        reader = PdfReader(pdf_path)
        text = []
        
        for page_num, page in enumerate(reader.pages, 1):
            page_text = page.extract_text()
            if page_text:
                text.append(f"--- Page {page_num} ---\n")
                text.append(page_text)
                text.append("\n\n")
        
        return "".join(text)
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None


def process_pdfs(pdf_dir):
    """
    Process all PDF files in the specified directory.
    
    Args:
        pdf_dir: Directory containing PDF files
    """
    pdf_dir = Path(pdf_dir)
    
    if not pdf_dir.exists():
        print(f"Directory {pdf_dir} does not exist!")
        return
    
    # Find all PDF files
    pdf_files = list(pdf_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"No PDF files found in {pdf_dir}")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s)")
    print("-" * 50)
    
    for pdf_path in sorted(pdf_files):
        print(f"Processing: {pdf_path.name}")
        
        # Extract text
        text = extract_text_from_pdf(pdf_path)
        
        if text:
            # Create output path with .txt extension
            txt_path = pdf_path.with_suffix(".txt")
            
            # Write to file
            try:
                with open(txt_path, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"  ✓ Saved to: {txt_path.name}")
            except Exception as e:
                print(f"  ✗ Error saving {txt_path}: {e}")
        else:
            print(f"  ✗ Failed to extract text")
        
        print()
    
    print("-" * 50)
    print("Processing complete!")


if __name__ == "__main__":
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    pdf_directory = script_dir / "pdfs"
    
    print(f"PDF Directory: {pdf_directory}")
    print()
    
    process_pdfs(pdf_directory)
