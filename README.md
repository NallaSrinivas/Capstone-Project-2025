# SkillForge: Multi-Agent Learning Platform

A sophisticated multi-agent AI system built with Google's ADK (Agent Development Kit) that provides intelligent tutoring, research, file management, and quiz capabilities. SkillForge orchestrates multiple specialized agents to deliver a comprehensive learning experience.

## 🎯 Overview

SkillForge is an intelligent learning platform powered by Google Gemini 2.5 Flash Lite that uses a multi-agent architecture. Each agent is specialized for a specific task:

- **SkillForge (Root Agent)**: Main orchestrator that routes requests to appropriate agents
- **Tutor Agent**: Explains topics, creates study guides, and generates learning materials
- **Librarian Agent**: Performs real-time research using Google Search
- **Secretary Agent**: Manages file I/O operations and document management
- **Quiz Agent**: Creates quizzes and evaluates student responses

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Examples](#examples)

## ✨ Features

### Core Capabilities

- **Interactive Chat Interface**: Async-based chat loop with streaming responses
- **Multi-Agent System**: Specialized agents for different learning tasks
- **Session Management**: SQLite-based session persistence with user tracking
- **File Processing**: Read and write files in multiple formats (Markdown, PDF, DOCX)
- **Research Integration**: Real-time web search via Librarian Agent
- **Quiz Generation**: Dynamic quiz creation and grading
- **Streaming Responses**: Real-time streaming of agent responses with tool call tracking

### Supported File Formats

- **Input**: PDF, DOCX, TXT, MD, Python files
- **Output**: Markdown (`.md`), PDF (`.pdf`), DOCX (`.docx`)

### Supported File Operations

- Read up to 3 files simultaneously
- Save documents with automatic timestamps
- Convert content between formats

## 📁 Project Structure

```
KAGGLE/
├── main.py                          # Main entry point and chat loop
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── app/
│   ├── __init__.py
│   ├── agent.py                     # Multi-agent definitions
│   ├── exception/
│   │   ├── exception.py             # Custom exception handling
│   │   └── text.py                  # Exception text constants
│   ├── logger/
│   │   ├── __init__.py
│   │   └── logging.py               # Logging configuration
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── file_maker.py            # File writing utilities (PDF, DOCX, MD)
│   │   ├── file_reader.py           # File reading utilities
│   │   └── python_show.py           # Python code display tool
│   └── utils/
│       └── db.py                    # Database utilities
├── experiments/                     # Jupyter notebooks for exploration
│   ├── day1a.ipynb
│   ├── day1b.ipynb
│   ├── day2a.ipynb
│   ├── day-2b-agent-tools-best-practices.ipynb
│   ├── day-3a-agent-sessions.ipynb
│   ├── day-3b-agent-memory.ipynb
│   ├── day-4a-agent-observability.ipynb
│   ├── day-4b-agent-evaluation.ipynb
│   ├── day-5a-agent2agent-communication.ipynb
│   ├── day-5b-agent-deployment.ipynb
│   └── sample-agent/
├── uploads/                         # Input files for reading
├── outputs/                         # Generated output files
└── temp/                            # Temporary working directory
```

## 🚀 Installation

### Prerequisites

- Python 3.10+
- Virtual environment (recommended)
- Google Cloud credentials
- API keys configured

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone <repo-url>
   cd KAGGLE
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv kenv
   kenv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## ⚙️ Configuration

### Environment Variables

- `GOOGLE_API_KEY`: Required for Google Gemini API access
- Database URL: `sqlite+aiosqlite:///agents.db` (default)

### Database Setup

The system automatically creates a SQLite database (`agents.db`) with session management. Sessions are tracked by:
- `app_name`: "skillforge"
- `user_id`: User identifier
- `session_id`: Session tracking ID

### Model Configuration

All agents use **Gemini 2.5 Flash Lite** with the following retry strategy:
- Max attempts: 5
- Exponential base: 7
- Initial delay: 1 second
- Retryable status codes: 429, 500, 503, 504

## 📖 Usage

### Running the Application

```bash
python main.py
```

### Interaction Flow

1. Start the application
2. Enter a session ID (or use default)
3. Type your learning request
4. The Root Agent routes to appropriate agents
5. Get streamed responses with tool execution tracking
6. Type 'exit' or 'quit' to end

### Example Commands

**For Learning:**
```
"Explain machine learning concepts"
"Create a study guide on quantum physics"
"Generate a summary of climate change"
```

**For Research:**
```
"What are the latest developments in AI?"
"Research blockchain technology for me"
```

**For Quizzes:**
```
"Create a quiz on biology"
"Generate MCQs about world history"
```

**For File Operations:**
```
"Create a PDF study guide on Python"
"Save a markdown summary on data structures"
"Read the file in uploads/notes.pdf"
```

## 🏗️ Architecture

### Agent Hierarchy

```
SkillForge (Root Agent)
├── Tutor Agent
│   ├── Librarian Agent
│   └── Secretary Agent
├── Quiz Agent
│   ├── Tutor Agent
│   ├── Secretary Agent
│   └── Librarian Agent
└── Secretary Agent
    └── Librarian Agent
```

### Request Routing Logic

| Request Type | Routed To | Secondary Agents |
|---|---|---|
| Learning requests | Tutor Agent | Librarian, Secretary |
| Quiz creation/grading | Quiz Agent | Tutor, Secretary, Librarian |
| File operations | Secretary Agent | Librarian |
| Research questions | Tutor Agent | Librarian, Secretary |

### Communication Flow

1. **User Input** → Main chat loop
2. **Root Agent** → Analyzes request and routes
3. **Specialized Agent** → Processes request, may call sub-agents
4. **Tool Execution** → File I/O, web search, etc.
5. **Response Streaming** → Async streaming back to user
6. **Session Persistence** → Stored in SQLite database

## 🔧 API Reference

### Core Agents

#### Librarian Agent
```python
librarian_agent = Agent(
    name="librarian_agent",
    description="A research specialist that retrieves real-time information.",
    tools=[google_search]
)
```
- **Tools**: Google Search
- **Output Key**: `librarian_response`

#### Secretary Agent
```python
secretary_agent = Agent(
    name="secretary_agent",
    description="Handles file reading, writing, note-saving, and document management.",
    tools=[FunctionTool(read_local_files), FunctionTool(save_file), AgentTool(librarian_agent)]
)
```
- **Tools**: read_local_files, save_file, librarian_agent
- **Output Key**: `secretary_response`

#### Tutor Agent
```python
tutor_agent = Agent(
    name="tutor_agent",
    description="A structured tutor who teaches topics, creates study guides, and generates learning materials.",
    tools=[AgentTool(librarian_agent), AgentTool(secretary_agent)]
)
```
- **Tools**: librarian_agent, secretary_agent
- **Output Key**: `tutor_response`

#### Quiz Agent
```python
quiz_agent = Agent(
    name="quiz_agent",
    description="Creates quizzes, evaluates answers, and helps learners practice.",
    tools=[AgentTool(tutor_agent), AgentTool(secretary_agent), AgentTool(librarian_agent)]
)
```
- **Tools**: tutor_agent, secretary_agent, librarian_agent
- **Output Key**: `quiz_response`

### Custom Tools

#### `save_file(topic: str, content: str, name_file: str, file_format: str = "md") -> dict`

Saves content to the `/outputs` directory.

**Parameters:**
- `topic` (str): Document title/topic
- `content` (str): Document content
- `name_file` (str): Filename without extension
- `file_format` (str): Format - "md" (default), "pdf", or "docx"

**Returns:**
```python
{
    "success": bool,
    "message": str,
    "filepath": str
}
```

#### `read_local_files(file_paths: str, tool_context: ToolContext) -> dict`

Reads content from files in the `/uploads` directory.

**Parameters:**
- `file_paths` (str): Comma-separated filenames
- `tool_context` (ToolContext): ADK context

**Supported Formats:**
- `.pdf`, `.docx`, `.txt`, `.md`, `.py`

**Returns:**
```python
{
    "success": bool,
    "files": [
        {
            "filename": str,
            "status": "ok" | "error",
            "content": str
        }
    ]
}
```

**Limitations:**
- Maximum 3 files per request
- Files must be in `/uploads` directory

## 💡 Examples

### Example 1: Get a Study Guide

**User Input:**
```
Create a comprehensive study guide on photosynthesis and save it as PDF
```

**Flow:**
1. Root Agent → Routes to Tutor Agent
2. Tutor Agent → Creates structured guide
3. Secretary Agent → Saves as PDF in `/outputs`

**Output:**
- File created: `/outputs/photosynthesis_study_guide.pdf`

### Example 2: Research and Quiz

**User Input:**
```
Research the latest AI trends and create a quiz about them
```

**Flow:**
1. Root Agent → Routes to Tutor Agent
2. Tutor Agent → Calls Librarian Agent for latest info
3. Quiz Agent → Creates quiz based on research
4. Returns interactive quiz questions

### Example 3: File Processing

**User Input:**
```
Read the notes in uploads/biology_notes.pdf and create a summary
```

**Flow:**
1. Root Agent → Routes to Secretary Agent
2. Secretary Agent → Reads PDF from `/uploads`
3. Tutor Agent → Creates summary
4. Returns summary content

## 📊 Session Management

Sessions are stored in SQLite with the following structure:

- **app_name**: "skillforge" (constant)
- **user_id**: Unique user identifier
- **session_id**: Session number for tracking
- **created_at**: Timestamp
- **messages**: Conversation history

## 🔐 Security Considerations

- API keys stored in `.env` (not committed to git)
- File operations limited to `/uploads` and `/outputs`
- Maximum 3 files readable per request
- Tool execution tracked and logged
- Custom exception handling for errors

## 📝 Logging

Logging is configured in `app/logger/logging.py`:
- Level: INFO
- Tracks agent activities, tool calls, and responses
- All interactions logged to console

## 🛠️ Troubleshooting

### API Connection Issues
- Verify `GOOGLE_API_KEY` in `.env`
- Check internet connectivity
- Ensure API quotas not exceeded

### File Not Found
- Ensure files are in `/uploads` directory
- Check filename spelling and extension
- Maximum 3 files per request

### Session Issues
- Database file should auto-create
- Check write permissions in project root
- Clear `agents.db` if corrupted

## 📚 Experiments

Jupyter notebooks in `/experiments` folder demonstrate:
- Agent tool best practices
- Session management
- Agent memory patterns
- Observability and monitoring
- Agent-to-agent communication
- Deployment strategies

## 🤝 Contributing

1. Create feature branch
2. Make changes with clear commits
3. Test thoroughly
4. Submit pull request

## 📄 License

See LICENSE file for details

## 📞 Support

For issues or questions:
- Check the experiments folder for examples
- Review agent instructions in `app/agent.py`
- Check logs for detailed error messages

## 🎓 Learning Path

1. **Start**: Run `main.py` and interact with the chat
2. **Explore**: Check `/experiments` notebooks
3. **Extend**: Add custom tools in `/app/tools`
4. **Deploy**: Use deployment patterns from `day-5b-agent-deployment.ipynb`

---

**Project**: Capstone Project 2025  
**Author**: Nalla Srinivas  
**Repository**: Capstone-Project-2025  
**Branch**: main  
**Last Updated**: December 2025
