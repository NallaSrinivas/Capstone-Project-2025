import os
import asyncio
from dotenv import load_dotenv

from google.adk.agents import Agent
from google.adk.tools import google_search, AgentTool, FunctionTool
from google.genai import types
from google.adk.runners import InMemoryRunner
from google.adk.models.google_llm import Gemini

# Custom Tools
from .tools.file_maker import save_file
from .tools.file_reader import read_local_files

# Load environment variables
load_dotenv(".env")

# Retry strategy for all LLM calls
retry_config = types.HttpRetryOptions(
    attempts=5,
    exp_base=7,
    initial_delay=1,
    http_status_codes=[429, 500, 503, 504]
)

# ==========================================================
# =============== 1. LIBRARIAN AGENT =======================
# ==========================================================

librarian_agent = Agent(
    name="librarian_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="A research specialist that retrieves real-time information.",
    instruction="""
        You are a professional research librarian.

        - Use the Google Search tool to gather accurate, up-to-date information.
        - You MUST cite your findings clearly.
        - Keep responses concise unless asked otherwise.
        - Your output will be used by another agent — be structured & factual.

        Never hallucinate. If data is not available, say so.
    """,
    tools=[google_search],
    output_key="librarian_response"
)


# ==========================================================
# =============== 2. SECRETARY AGENT =======================
# ==========================================================

secretary_agent = Agent(
    name="secretary_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="Handles file reading, writing, note-saving, and document management.",
    instruction="""
        You are the Study Secretary.

        YOU MUST FOLLOW THESE RULES:
        1. For reading any files → ALWAYS use `read_local_files`.
        2. For saving any notes, summaries, reports, or study material:
            - Use `save_file`.
            - Detect requested format:
                • "pdf" → file_format='pdf'
                • "docx" / "word" → file_format='docx'
                • Otherwise → 'md'
        3. Never rewrite or improve content unless explicitly asked.
        4. Your job is execution (IO), not teaching. For explanations → send the task back to the Tutor.

        KEEP OUTPUT SHORT — tool results only.
    """,
    tools=[
        FunctionTool(read_local_files),
        FunctionTool(save_file),
        AgentTool(librarian_agent)
    ],
    output_key="secretary_response"
)


# ==========================================================
# =============== 3. TUTOR AGENT ===========================
# ==========================================================

tutor_agent = Agent(
    name="tutor_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="A structured tutor who teaches topics, creates study guides, and generates learning materials.",
    instruction="""
        You are a knowledgeable Tutor.

        YOUR TASKS:
        - Explain topics step-by-step.
        - Create study guides, summaries, examples, exercises.
        - Use the Librarian for real-time research.
        - Use the Secretary for file operations.

        RULES:
        - When user asks for a saved document (PDF, DOCX, etc.):
          → produce clean structured content
          → then delegate saving to secretary_agent
        - Be clear, accurate, and beginner-friendly.
    """,
    tools=[
        AgentTool(librarian_agent),
        AgentTool(secretary_agent)
    ],
    output_key="tutor_response"
)


# ==========================================================
# =============== 4. QUIZ AGENT ============================
# ==========================================================

quiz_agent = Agent(
    name="quiz_agent",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="Creates quizzes, evaluates answers, and helps learners practice.",
    instruction="""
        You are a Quiz Master.

        DUTIES:
        - Generate quizzes: MCQs, short answers, scenario questions, etc.
        - Grade user's answers with reasoning.
        - Use Secretary for reading any study materials or saving quiz results.
        - Use Tutor if you require topic explanations or context.
        - Ensure quizzes match the user’s current skill level.

        KEEP OUTPUT STRUCTURED:
        - Clear numbering
        - Difficulty labels
        - Provide answer keys only if asked
    """,
    tools=[
        AgentTool(tutor_agent),
        AgentTool(secretary_agent),
        AgentTool(librarian_agent),
    ],
    output_key="quiz_response"
)


# ==========================================================
# =============== 5. ROOT ORCHESTRATOR =====================
# ==========================================================

root_agent = Agent(
    name="SkillForge",
    model=Gemini(
        model="gemini-2.5-flash-lite",
        retry_options=retry_config
    ),
    description="The main interface for SkillForge. Routes user requests to the correct agent.",
    instruction="""
        You are SkillForge — a routing and orchestration agent.

        ROUTING RULES:
        ✔ Learning, explaining, study guides → tutor_agent  
        ✔ Research requests → tutor_agent (who may call librarian)  
        ✔ File operations → secretary_agent (but usually via tutor)  
        ✔ Quizzes → quiz_agent  

        CRITICAL FILE RULE:
        If the user asks:
            - "save file", "create PDF", "make docx", "export notes"
        You MUST:
            → send the task to tutor_agent with a message:
               "Generate the study content and delegate saving to secretary_agent."

        Never answer with content yourself. Always route.
    """,
    tools=[
        AgentTool(tutor_agent),
        AgentTool(quiz_agent),
        AgentTool(secretary_agent)
    ]
)
