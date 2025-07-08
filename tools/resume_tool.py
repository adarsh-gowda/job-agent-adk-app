"""
Resume Tool

This tool extracts and formats resume content from a given PDF file.
"""

import os
import time
import shutil
from typing import Dict, Any
import pdfplumber


def extract_resume_text(file_path: str = "data/resume.pdf") -> Dict[str, Any]:
    """
    Extracts text from a resume PDF and returns it in a structured ADK format.

    Args:
        file_path (str): Path to the resume PDF

    Returns:
        Dict[str, Any]: Structured resume data
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with pdfplumber.open(file_path) as pdf:
            pages = [page.extract_text() for page in pdf.pages]
            resume_text = "\n".join(p for p in pages if p)

        word_count = len(resume_text.split())
        page_count = len(pages)

        return {
            "result": resume_text,
            "stats": {
                "file": os.path.basename(file_path),
                "word_count": word_count,
                "page_count": page_count
            },
            "additional_info": {
                "format": "pdf",
                "status": "success",
                "timestamp": time.time()
            }
        }

    except Exception as e:
        return {
            "result": "Failed to extract resume text.",
            "stats": {"file": os.path.basename(file_path) if file_path else None},
            "additional_info": {
                "status": "error",
                "error_type": type(e).__name__,
                "message": str(e)
            }
        }

class ResumeTool:
    """
    ResumeTool class for enhancing resumes based on a job description.
    """

    def __init__(self, resume_path: str = "data/resume.pdf"):
        self.original_path = resume_path
        self.updated_path = "data/resume_updated.pdf"

        # Ensure data folder exists
        os.makedirs(os.path.dirname(self.updated_path), exist_ok=True)

    def enhance_resume_with_jd(self, job_description: str) -> str:
        """
        Simulates enhancing the resume based on job description.
        Creates a copy as a placeholder for an enhanced resume.

        Returns:
            str: Path to the updated resume.
        """
        print(f"[Placeholder] Enhancing resume for JD: {job_description[:60]}...")

        # Check if original resume exists
        if not os.path.exists(self.original_path):
            raise FileNotFoundError(f"Original resume not found: {self.original_path}")

        # If updated resume already exists, just return it
        if os.path.exists(self.updated_path):
            print(f"✔️ Resume already enhanced at: {self.updated_path}")
            return self.updated_path

        # Copy the original to create a new "enhanced" version
        shutil.copyfile(self.original_path, self.updated_path)
        print(f"✅ Created updated resume: {self.updated_path}")

        return self.updated_path

