from google.adk.tools.base import Tool, tool
import pdfplumber

@tool(name="ResumeTool", description="Extracts text from the user's resume PDF.")
class ResumeTool(Tool):
    def run(self, resume_path: str) -> str:
        try:
            with pdfplumber.open(resume_path) as pdf:
                text = "\n".join(page.extract_text() for page in pdf.pages if page.extract_text())
            return text.strip()
        except Exception as e:
            return f"Error reading resume: {str(e)}"

