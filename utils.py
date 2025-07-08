"""
Utils - Async wrapper for ADK agent calls
"""

from google.adk.runners import Runner


async def call_agent_async(runner: Runner, user_id: str, session_id: str, user_input: str) -> None:
    """
    Calls an agent asynchronously using ADK's Runner and prints the response.

    Args:
        runner (Runner): Initialized ADK runner with the agent and session.
        user_id (str): The user ID.
        session_id (str): The session ID for state tracking.
        user_input (str): User's query/input for the agent.
    """
    try:
        result = await runner.run(user_id=user_id, session_id=session_id, input=user_input)

        if isinstance(result, str):
            print(f"🤖 Agent: {result}")
        elif isinstance(result, dict) and "output" in result:
            print(f"🤖 Agent: {result['output']}")
        else:
            print(f"🤖 Agent returned unrecognized format:\n{result}")

    except Exception as e:
        print(f"❌ Error while calling agent: {e}")
