import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner

async def main():
    root_agent = Agent(
            name="test_agent",
            # https://ai.google.dev/gemini-api/docs/models
            model="gemini-2.0-flash",
            description="test agent",
            instruction="""
            Say hello to the user.
            """,
)
    runner = Runner(agent=root_agent, app_name="test-runner", session_service="memory")

    result = await runner.arun({})
    print("✅ Result:", result)

if __name__ == "__main__":
    asyncio.run(main())

