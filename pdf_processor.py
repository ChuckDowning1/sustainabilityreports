"""
PDF Processor module for extracting and preprocessing text from sustainability reports.
"""

import os
from typing import List, Dict, Any
import PyPDF2


class PDFProcessor:
    """Handles reading and preprocessing of PDF files."""
    
    def __init__(self, chunk_size: int = 100000, overlap: int = 2000):
        """
        Initialize the PDF processor.
        
        Args:
            chunk_size: Maximum number of characters per chunk
            overlap: Overlap between chunks to maintain context
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract all text from a PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            The extracted text as a string
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        text = ""
        with open(pdf_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n\n"
        
        return text
    
    def chunk_text(self, text: str) -> List[str]:
        """
        Split text into manageable chunks for the LLM.
        
        Args:
            text: The full text to chunk
            
        Returns:
            List of text chunks
        """
        if not text:
            return []
        
        # For very short documents, just return the whole text as one chunk
        if len(text) <= self.chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            
            # Adjust the end to avoid cutting words
            if end < len(text):
                # Try to find a good breaking point
                breaking_chars = ["\n\n", "\n", ". ", "? ", "! ", ", "]
                for char in breaking_chars:
                    pos = text[start:end].rfind(char)
                    if pos != -1:
                        end = start + pos + len(char)
                        break
            
            chunks.append(text[start:end])
            start = end - self.overlap if end < len(text) else end
        
        return chunks
    
    def process_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Process a PDF file, extracting and chunking its content.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dict with metadata and text chunks
        """
        filename = os.path.basename(pdf_path)
        company_name = os.path.splitext(filename)[0]
        
        try:
            full_text = self.extract_text(pdf_path)
            text_chunks = self.chunk_text(full_text)
            
            return {
                "company": company_name,
                "file_path": pdf_path,
                "total_chunks": len(text_chunks),
                "text_chunks": text_chunks,
                "full_text_length": len(full_text)
            }
        except Exception as e:
            print(f"Error processing PDF {pdf_path}: {str(e)}")
            return {
                "company": company_name,
                "file_path": pdf_path,
                "error": str(e)
            } 