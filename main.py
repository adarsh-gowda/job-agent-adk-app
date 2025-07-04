from google.adk.agents.llm_agent import Agent
from google.adk.server import run_agent_server
from agents.matcher_agent import JDMatcherAgent

if __name__ == "__main__":
    run_agent_server(agent=JDMatcherAgent())
