# Comprehensive System and Tooling Documentation

This document provides a detailed inventory of the tools, libraries, technologies, and APIs available within the sandboxed execution environment.

## 1. System Environment Overview

| Component | Detail |
| :--- | :--- |
| **Operating System** | Ubuntu 22.04 linux/amd64 |
| **User** | `ubuntu` (with `sudo` privileges) |
| **Home Directory** | `/home/ubuntu` |
| **Python Version** | 3.11.0rc1 |
| **Node.js Version** | v22.13.0 |
| **Package Managers** | `pip3` (Python), `npm`, `pnpm` (Node.js) |

## 2. Core Toolset (Function Calls)

The primary method of interaction with the environment is through a set of specialized function-calling tools. These tools abstract complex operations into simple, structured commands.

| Tool Name | Purpose | Key Actions |
| :--- | :--- | :--- |
| `plan` | Task management and planning | `update`, `advance` |
| `message` | User communication and result delivery | `info`, `ask`, `result` |
| `shell` | Command-line execution | `exec`, `wait`, `view`, `send`, `kill` |
| `file` | File system content manipulation | `read`, `write`, `append`, `edit`, `view` |
| `match` | File and content searching | `glob` (file paths), `grep` (file content) |
| `search` | External information retrieval | `info`, `image`, `api`, `news`, `tool`, `data`, `research` |
| `schedule` | Task scheduling | `cron`, `interval` |
| `expose` | Public port exposure | N/A (requires port number) |
| `browser` | Web navigation | `navigational`, `informational`, `transactional` |
| `generate` | Media generation mode | N/A (enters a sub-mode) |
| `slides` | Presentation creation mode | N/A (enters a sub-mode) |
| `webdev_init_project` | Web project scaffolding | `web-static`, `web-db-user` |

## 3. Custom Command-Line Utilities

The environment includes several custom utilities for specialized tasks, which are wrappers around underlying APIs and technologies.

| Utility Command | Description | Underlying Technology/API |
| :--- | :--- | :--- |
| `manus-render-diagram` | Renders diagram files (.mmd, .d2, .puml, .md) to PNG format. | Diagramming engine (e.g., Mermaid, D2, PlantUML) |
| `manus-md-to-pdf` | Converts Markdown files to PDF format. | PDF rendering engine (e.g., WeasyPrint, xhtml2pdf) |
| `manus-speech-to-text` | Transcribes speech/audio/video files to text. | Speech-to-Text API (e.g., Whisper, proprietary service) |
| `manus-mcp-cli` | Command-line interface for Model Context Protocol (MCP) servers. | MCP API |
| `manus-upload-file` | Uploads a file to S3 and returns a public URL. | AWS S3 or compatible object storage API |
| `manus-export-slides` | Exports slides from a `manus-slides://` URI to PDF or PPT format. | Slides generation API |

## 4. API Access and Configuration

The environment is pre-configured for access to external services, primarily through environment variables.

| Service | Environment Variables | Configuration Details |
| :--- | :--- | :--- |
| **OpenAI-Compatible LLM** | `OPENAI_API_KEY`, `OPENAI_BASE_URL`, `OPENAI_API_BASE` | Access to various LLMs (`gpt-4.1-mini`, `gpt-4.1-nano`, `gemini-2.5-flash`) via a unified, proxy-based OpenAI API endpoint. |

## 5. Installed Libraries and Technologies

### Python (via `pip3`)

The Python environment is rich with libraries for data science, web development, and document processing.

| Category | Key Libraries | Purpose |
| :--- | :--- | :--- |
| **Web/API** | `fastapi`, `flask`, `uvicorn`, `requests`, `httpx` | Building web applications, APIs, and making HTTP requests. |
| **Data Science** | `numpy`, `pandas`, `seaborn`, `matplotlib`, `plotly`, `narwhals` | Numerical computation, data manipulation, and visualization. |
| **Document Processing** | `fpdf2`, `reportlab`, `weasyprint`, `xhtml2pdf`, `openpyxl`, `pdf2image`, `pyhanko` | PDF generation, HTML/Markdown to PDF conversion, Excel handling, image processing, and digital signing. |
| **Web Scraping** | `beautifulsoup4`, `lxml`, `cssselect2` | HTML parsing and data extraction. |
| **LLM/AI** | `openai` | Client for interacting with the configured LLM API. |
| **Utility** | `pydantic`, `jinja2`, `tqdm`, `typing-extensions` | Data validation, templating, progress bars, and type hinting. |
| **Cloud/AWS** | `boto3`, `botocore`, `s3transfer` | AWS SDK for Python, used for interacting with services like S3. |

### Node.js (via `npm`/`pnpm`)

The Node.js environment is minimal, focusing on package management.

| Component | Version | Purpose |
| :--- | :--- | :--- |
| **Node.js** | v22.13.0 | Runtime environment for JavaScript execution. |
| **pnpm** | 10.20.0 | Fast, disk-space efficient package manager. |
| **npm** | 10.9.2 | Default Node.js package manager. |
| **corepack** | 0.30.0 | Manages package manager versions. |
