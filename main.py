import asyncio
import os
from tools.job_scraper_tool import get_job_description
from tools.resume_tool import ResumeTool
from tools.tracker_tool import track_application, log_applied_job

from agents.matcher_agent import resume_matcher_agent
from agents.cover_letter_agent import cover_letter_agent
from agents.application_agent import application_agent

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content
from google.adk.sessions import Session
# from google.adk.core import InvocationContext  # <-- Make sure this import is correct for your ADK

matcher_runner = Runner(agent=resume_matcher_agent, app_name="resume-matcher", session_service=InMemorySessionService())

async def run_job_application(job_url: str):
    print(f"\nScraping job from: {job_url}")
    job_data = await get_job_description(job_url)

    if not job_data["stats"]["success"]:
        print(f"Failed to scrape job: {job_data['additional_info'].get('error')}")
        return

    jd = job_data["result"]["description"]
    title = job_data["result"]["job_title"]
    company = job_data["result"]["company"]

    print(f"\n📄 Job Title: {title}\n🏢 Company: {company}\n📝 Description (trimmed): {jd[:300]}...\n")

    # Step 1: Match JD with Resume
    resume_path = "data/resume.pdf"
    print("🔗 Matching resume with job description...")

    # Try creating the session using the session_service directly
    # matcher_runner.session_service.create_session({
    #     "user_id": "adarsha",
    #     "session_id": "resume-matcher"
    # })

    content = Content(
        role="user",
        parts=[
            {"text": f"Job Title: {title}"},
            {"text": f"Job Description: {jd}"},
            {"text": f"Resume Path: {resume_path}"}
        ]
    )

    session = Session(user_id="adarsha", session_id="resume-matcher")
    matcher_runner.session_service.create_session(session)

    async for event in matcher_runner.run_async(
        user_id="adarsha",
        session_id="resume-matcher",
        new_message=content
    ):
        print("[DEBUG matcher_runner event]", event)

    # Step 3: Generate Cover Letter
    print("✍️ Generating cover letter...")
    # cover_context = InvocationContext( # This line was removed as per the new_code
    #     user_id="adarsha",
    #     session_id="cover-letter",
    #     input={
    #         "job_title": title,
    #         "job_description": jd,
    #         "resume_path": resume_path
    #     }
    # )
    # async for event in cover_letter_agent.run_async(parent_context=cover_context): # This line was removed as per the new_code
    #     print("[DEBUG cover_letter_agent event]", event)

    # Step 4: Apply for Job
    print("🚀 Applying to job...")
    # application_context = InvocationContext( # This line was removed as per the new_code
    #     user_id="adarsha",
    #     session_id="application",
    #     input={
    #         "job_title": title,
    #         "job_description": jd,
    #         "resume_path": resume_path,
    #         "cover_letter": "[PLACEHOLDER_COVER_LETTER]"
    #     }
    # )
    # async for event in application_agent.run_async(parent_context=application_context): # This line was removed as per the new_code
    #     print("[DEBUG application_agent event]", event)

def main():
    job_urls = [
        "https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4259170161",
        "https://www.linkedin.com/jobs/collections/recommended/?currentJobId=4261728134",
    ]

    loop = asyncio.get_event_loop()
    for job_url in job_urls:
        loop.run_until_complete(run_job_application(job_url))

if __name__ == "__main__":
    main()
