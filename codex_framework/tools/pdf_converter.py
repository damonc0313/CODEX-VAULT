"""PDF to text conversion tool for knowledge integration."""

from pathlib import Path
from typing import List, Dict, Optional
import logging


def convert_pdf_to_text(pdf_path: Path) -> str:
    """
    Convert PDF to text using pypdf.
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Extracted text content
    """
    try:
        from pypdf import PdfReader
        
        reader = PdfReader(str(pdf_path))
        text_content = []
        
        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            if text.strip():
                text_content.append(f"--- Page {page_num} ---\n{text}\n")
                
        return "\n".join(text_content)
        
    except ImportError:
        return "Error: pypdf library not available"
    except Exception as e:
        return f"Error converting PDF: {str(e)}"


def convert_all_pdfs(
    input_dir: Path,
    output_dir: Path,
    pdf_files: Optional[List[str]] = None
) -> Dict[str, str]:
    """
    Convert multiple PDF files to text.
    
    Args:
        input_dir: Directory containing PDFs
        output_dir: Directory for text output
        pdf_files: Specific PDF files to convert (or all if None)
        
    Returns:
        Dictionary mapping PDF names to output paths
    """
    logger = logging.getLogger(__name__)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = {}
    
    # Get PDF files
    if pdf_files is None:
        pdfs = list(input_dir.glob("*.pdf"))
    else:
        pdfs = [input_dir / pdf for pdf in pdf_files]
        
    logger.info(f"Converting {len(pdfs)} PDF files...")
    
    for pdf_path in pdfs:
        if not pdf_path.exists():
            continue
            
        # Convert PDF to text
        text_content = convert_pdf_to_text(pdf_path)
        
        # Save to text file
        output_path = output_dir / f"{pdf_path.stem}.txt"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"SOURCE: {pdf_path.name}\n")
            f.write(f"CONVERTED: Codex Framework PDF Converter\n")
            f.write("=" * 70 + "\n\n")
            f.write(text_content)
            
        results[pdf_path.name] = str(output_path)
        logger.info(f"Converted: {pdf_path.name} → {output_path.name}")
        
    return results


if __name__ == "__main__":
    # Standalone conversion
    import sys
    
    if len(sys.argv) > 1:
        pdf_file = Path(sys.argv[1])
        text = convert_pdf_to_text(pdf_file)
        print(text)
    else:
        print("Usage: python pdf_converter.py <pdf_file>")
