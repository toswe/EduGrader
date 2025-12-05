import hashlib
import re
import requests
import logging
from pathlib import Path
from typing import Optional

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None

logger = logging.getLogger(__name__)

CACHE_DIR = Path(__file__).resolve().parents[2] / "pipeline" / "tmp" / "pdf_cache"


def extract_pdf(url: str, timeout: int = 30, verify_ssl: bool = False) -> Optional[str]:
    if not url:
        return None
    
    # If not a URL, return as-is
    if not re.match(r"^https?://", url):
        return url

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    # Generate cache key from URL
    key = hashlib.sha256(url.encode("utf-8")).hexdigest()
    pdf_path = CACHE_DIR / f"{key}.pdf"
    txt_path = CACHE_DIR / f"{key}.txt"

    # Return cached text if available
    if txt_path.exists():
        try:
            text = txt_path.read_text(encoding="utf-8")
            logger.debug(f"Using cached textbook text from {txt_path}")
            return text
        except Exception as e:
            logger.warning(f"Failed to read cached text from {txt_path}: {e}")

    # Download PDF if not cached
    if not pdf_path.exists():
        try:
            logger.debug(f"Downloading PDF from {url}...")
            resp = requests.get(url, timeout=timeout, verify=verify_ssl)
            resp.raise_for_status()
            pdf_path.write_bytes(resp.content)
            logger.debug(f"Downloaded PDF to {pdf_path}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download PDF from {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error downloading PDF: {e}")
            return None

    # Extract text from PDF
    try:
        if PdfReader is None:
            logger.error("PyPDF2 not available; cannot extract PDF text")
            return None
        
        logger.debug(f"Extracting text from {pdf_path}...")
        text_parts = []
        with open(pdf_path, "rb") as fh:
            reader = PdfReader(fh)
            logger.debug(f"PDF has {len(reader.pages)} pages")
            for i, page in enumerate(reader.pages):
                try:
                    extracted = page.extract_text() or ""
                    text_parts.append(extracted)
                except Exception as e:
                    logger.warning(f"Failed to extract text from page {i}: {e}")
                    continue
        
        text = "\n".join(t.strip() for t in text_parts if t is not None)
        if not text.strip():
            logger.warning(
                f"No text extracted from {pdf_path}; file may be scanned image or corrupted"
            )
        
        txt_path.write_text(text or "", encoding="utf-8")
        logger.debug(f"Successfully extracted and cached {len(text)} characters from PDF")
        return text
    except Exception as e:
        logger.error(f"Failed to extract text from PDF: {e}")
        return None
