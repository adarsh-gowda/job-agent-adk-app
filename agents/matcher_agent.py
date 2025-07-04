from google.adk.agents.llm_agent import Agent

MATCHER_PROMPT = """
You are a job matching assistant. Your task is to compare a resume with a job description and return a match score from 0–100 along with a short explanation.

Resume:
{resume}

Job Description:
{job_description}

Respond like:
Score: 87
Reason: Strong match in skills (Python, ML), but lacks leadership experience.
"""

class JDMatcherAgent(Agent):
    prompt = MATCHER_PROMPT
    tools = ["ResumeTool"]  # Tool we created earlier
