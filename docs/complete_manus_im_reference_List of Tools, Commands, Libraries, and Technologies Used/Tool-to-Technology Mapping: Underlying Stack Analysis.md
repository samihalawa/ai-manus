# Tool-to-Technology Mapping: Underlying Stack Analysis

This document provides a definitive mapping of each core tool's functionality to the specific libraries, frameworks, and APIs that enable it, based on the systematic technical analysis.

## 1. Core Tool Technology Breakdown

| Core Tool | Primary Function | Underlying Technologies & Libraries | Key APIs/Protocols |
| :--- | :--- | :--- | :--- |
| **`plan`** | Task Orchestration | Internal Agent Logic, State Management | N/A (Internal Protocol) |
| **`message`** | User Communication | Internal Messaging Protocol | N/A (Internal Protocol) |
| **`shell`** | Command Execution | Linux Kernel, Bash Shell, Python 3.11, Node.js 22 | N/A (OS/Runtime) |
| **`file`** | File System Ops | Linux File System (ext4), Python `os` module | N/A (OS/Runtime) |
| **`match`** | File/Content Search | Python `glob` module, Python `re` (Regex) module | N/A (OS/Runtime) |
| **`search`** | External Information | Proprietary Search Engine Backend | External Search API |
| **`browser`** | Web Automation | **Playwright** (v1.55.0), **Chromium** (Stable), Python `requests`, `httpx` | N/A (Web Standard) |
| **`expose`** | Public Networking | Reverse Proxy/Tunneling Service (e.g., Nginx/Cloudflare Tunnel concept) | Proprietary Tunneling API |
| **`schedule`** | Task Scheduling | Cron Daemon, Internal Task Queue | N/A (Internal Protocol) |
| **`generate`** | Media Creation | **OpenAI-compatible LLM API**, Proprietary Media Generation Models | External LLM API, Internal Media API |
| **`slides`** | Presentation Build | Internal Slides Generation Engine, Markdown Parser | Internal Slides API |
| **`webdev_init_project`** | Project Scaffolding | Python Scripting, Jinja2 (Templating), `fastapi`, `flask` (Frameworks) | N/A (Internal Scripting) |

## 2. Custom Utility Technology Breakdown

The custom command-line utilities are specialized wrappers that rely on specific installed libraries.

| Custom Utility | Primary Function | Underlying Technologies & Libraries |
| :--- | :--- | :--- |
| **`manus-upload-file`** | Cloud Storage | **`boto3`** (AWS SDK), **S3-compatible Object Storage** |
| **`manus-md-to-pdf`** | Document Conversion | **`weasyprint`** or **`xhtml2pdf`** (Python Libraries) |
| **`manus-render-diagram`** | Diagram Rendering | Mermaid, D2, PlantUML Engines |
| **`manus-speech-to-text`** | Transcription | **Whisper** or Proprietary Speech-to-Text API |
| **`manus-export-slides`** | Slides Export | Internal Slides API, PDF/PPT Generation Libraries |
| **`manus-mcp-cli`** | Protocol Interaction | **Model Context Protocol (MCP)** |

## 3. Core Supporting Technologies

These technologies are not tied to a single tool but form the foundation of the entire environment.

| Category | Technology | Key Libraries/Components | Role in System |
| :--- | :--- | :--- | :--- |
| **LLM Orchestration** | **OpenAI-compatible API** | `OPENAI_API_KEY`, `OPENAI_BASE_URL` | The central "brain" that calls all tools. |
| **Web Frameworks** | **Python Ecosystem** | `fastapi`, `flask`, `uvicorn`, `starlette` | Enables the agent to build and run its own web services. |
| **Data Persistence** | **SQLite** | Python `sqlite3` module | Provides file-based, persistent data storage for projects. |
| **Web Scraping** | **Python Ecosystem** | `beautifulsoup4`, `lxml`, `cssselect2` | Used by the agent's internal logic to process HTML content retrieved by the `browser` tool. |
