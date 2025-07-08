"""
Application Agent

This agent automates the process of applying to a job using browser automation.
"""

from google.adk.agents import LlmAgent
from tools.resume_tool import extract_resume_text
from tools.job_scraper_tool import get_job_description
from tools.browser_tool import apply_to_job
from tools.tracker_tool import track_application

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

application_agent = LlmAgent(
    name="ApplicationAgent",
    model=GEMINI_MODEL,
    instruction="""
You are an Autonomous Job Application Agent.

Steps:
1. Use 'get_job_description' with a search query to retrieve a live job post
2. Use 'extract_resume_text' to extract the candidate's resume content
3. Use 'apply_to_job' to apply for the job on behalf of the user
   - Submit resume, name, email if required
   - Use the job URL from the job scraper
4. After applying, call 'track_application' to log the application status and details

Format your final output like this:
Application Status: Success
Job Title: Data Scientist
Company: OpenAI
Applied via: LinkedIn
Tracker: Application logged successfully

IMPORTANT:
- Always call tools in this order: job → resume → apply → track
- DO NOT fabricate job content or resume content.
- Ensure all tools return valid outputs before applying.
""",
    description="Autonomously applies to a job and tracks the application using browser automation",
    tools=[
        get_job_description,
        extract_resume_text,
        apply_to_job,
        track_application,
    ],
    output_key="application_status",
)
