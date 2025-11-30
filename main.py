import os
import asyncio
from dotenv import load_dotenv

from google.adk.sessions import DatabaseSessionService
from google.adk.runners import Runner
from google.genai import types

from app.root_agent import root_agent   # ✅ YOUR agent file

# Load env
load_dotenv(".env")


async def main():

    print("💬 SkillForge Chat Active!")
    print("---------------------------")

    # ============================
    # 1. App Name MUST be stable
    # ============================
    APP_NAME = "skillforge" or "agents" # <--- IMPORTANT: Define explicitly

    # ============================
    # 2. User & Session
    # ============================
    user_id = "srinivas_01"
    session_id = input("Enter session id (default=1): ").strip() or "1"

    # ============================
    # 3. Database Session Service
    # ============================
    session_service = DatabaseSessionService(
        db_url="sqlite+aiosqlite:///app/utils/agents.db"
    )

    # Ensure session exists
    existing = await session_service.get_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id
    )

    if not existing:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=user_id,
            session_id=session_id
        )

    # ============================
    # 4. Create Runner
    # ============================
    runner = Runner(
        agent=root_agent,
        session_service=session_service,
        app_name=APP_NAME   # <--- FIX: Proper app name
    )

    print("Type 'exit' to quit.\n")

    # ============================
    # 5. Chat Loop
    # ============================
    while True:

        user_input = input("You: ")

        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        content = types.Content(
            role="user",
            parts=[types.Part(text=user_input)]
        )

        try:
            # Streaming response
            async for event in runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=content
            ):
                if event.content and event.content.parts:
                    for part in event.content.parts:

                        # A) Tool call
                        if part.function_call:
                            print(f"   ⚙️ Tool call: {part.function_call.name}")

                        # B) Text
                        text = getattr(part, "text", None)
                        if text and text.strip():
                            print(f"agents: {text}")

        except Exception as e:
            print(f"[ERROR] {e}")


if __name__ == "__main__":
    asyncio.run(main())
