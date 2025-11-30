import asyncio
from app.agent import root_agent
from google.adk.runners import InMemoryRunner
from google.genai import types

async def test_agent():
    print("🧪 Testing Root Agent Routing...")

    runner = InMemoryRunner(agent=root_agent)

    print("✅ Runner created.")
    response = await runner.run_debug(
    "What is Agent Development Kit from Google? What languages is the SDK available in?"
)

    # ✔ Correct for your ADK version (positional argument)

    print("\nResponse received!\n")
    final_event = response[-1]          # last Event in the list
    parts = final_event.content.parts   # list of Part objects

    for part in parts:
        if part.text:
            print("\nFINAL OUTPUT:\n", part.text)


if __name__ == "__main__":
    asyncio.run(test_agent())