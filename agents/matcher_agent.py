"""
Resume Matcher Agent

This agent compares a resume to a job description and provides a match score and reasoning.
"""

from google.adk.agents import LlmAgent

from tools.resume_tool import extract_resume_text

# --- Constants ---
GEMINI_MODEL = "gemini-2.0-flash"

# Resume Matcher Agent
resume_matcher_agent = LlmAgent(
    name="ResumeMatcherAgent",
    model=GEMINI_MODEL,
    instruction="""
You are a Resume Matcher Agent.

Your role is to:
1. Use the 'extract_resume_text' tool to extract the full text content from the given resume.
2. Compare the extracted resume text with the job description provided below.
3. Return a score between 0 and 100 that represents how well the resume aligns with the job description.
4. Write 2–3 bullet points explaining your evaluation (why the score is what it is).
5. List any clearly missing but expected skills or experiences.
6. Return a JSON object with the following fields:

- match_score (integer from 0 to 100): How well the resume matches the job description
- reasons (list of 2–3 bullet points): Why you assigned this score
- missing (list): Key skills or experiences expected in the job description but missing from the resume

Here is the job description to compare with:

---
{{job_description}}
---

Return your answer in the following format:

Score: <integer between 0 and 100>

Reasons:
- <reason 1>
- <reason 2>
- <reason 3> (optional)

Missing:
- <missing skill or requirement>
- <another missing item> (if any)

Use the following example as a guide:

```json
{
  "match_score": 87,
  "reasons": [
    "Strong alignment in Python and ML skills",
    "Resume mentions 3+ years of experience as requested",
    "Slight gap in cloud deployment experience"
  ],
  "missing": [
    "AWS or GCP deployment",
    "Docker/Kubernetes experience"
  ]
}

""",
    description="Compares resume content to a job description and scores the match",
    tools=[extract_resume_text],
    output_key="match_report",
)
