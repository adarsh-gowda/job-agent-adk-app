"""
Cover Letter Agent

This agent generates a personalized, professional cover letter using the resume and job description.
"""

from google.adk.agents import LlmAgent
from tools.resume_tool import extract_resume_text
from tools.job_scraper_tool import get_job_description

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

cover_letter_agent = LlmAgent(
    name="CoverLetterAgent",
    model=GEMINI_MODEL,
    instruction="""
You are a Cover Letter Generator Agent.

Your task is to:
1. Use the 'extract_resume_text' tool to extract the resume content
2. Use the 'get_job_description' tool to retrieve a job post based on the user's query
3. Write a professional 3-paragraph cover letter that:
    - Highlights the candidate's skills and experience from the resume
    - Aligns specifically with the job requirements
    - Is clear, personalized, and free of generic statements

You must call both tools.

Use this structure:
- Paragraph 1: Greeting and introduction
- Paragraph 2: Skills and relevance to the job
- Paragraph 3: Closing with enthusiasm and availability

The tools return:
- 'extract_resume_text': result (resume text), stats, and metadata
- 'get_job_description': result (job title, company, description)

DO NOT make up job or resume info. Always extract and use real content.
""",
    description="Generates a customized cover letter for a scraped job using user's resume",
    tools=[extract_resume_text, get_job_description],
    output_key="cover_letter",
)
