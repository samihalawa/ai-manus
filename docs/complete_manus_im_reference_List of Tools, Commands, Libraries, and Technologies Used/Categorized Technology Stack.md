# Categorized Technology Stack

This document lists the specific libraries, frameworks, and APIs identified in the environment, categorized by their primary function.

## 1. Web Development and Server

These technologies are used for building and running web applications and APIs.

| Category | Technology | Type | Purpose |
| :--- | :--- | :--- | :--- |
| **Framework** | `fastapi` | Python Library | High-performance web framework for building APIs. |
| **Framework** | `flask` | Python Library | Lightweight web framework for general web applications. |
| **Server** | `uvicorn` | Python Library | ASGI server, typically used to run FastAPI/Starlette applications. |
| **Networking** | `expose` (Tool) | Core Tool | Creates temporary public tunnels for local ports. |
| **Networking** | `httpx` | Python Library | Modern, async-friendly HTTP client. |
| **Networking** | `requests` | Python Library | Standard HTTP client for making web requests. |

## 2. Data Science and Analysis

These libraries are fundamental for numerical computation, data manipulation, and visualization.

| Category | Technology | Type | Purpose |
| :--- | :--- | :--- | :--- |
| **Computation** | `numpy` | Python Library | Core library for numerical operations and array manipulation. |
| **Manipulation** | `pandas` | Python Library | Data structures and analysis tools (DataFrames). |
| **Manipulation** | `narwhals` | Python Library | Data manipulation library (potential alternative to Pandas). |
| **Visualization** | `seaborn` | Python Library | Statistical data visualization built on Matplotlib. |
| **Visualization** | `matplotlib` | Python Library | Comprehensive library for creating static, animated, and interactive visualizations. |
| **Visualization** | `plotly` | Python Library | Interactive graphing library. |

## 3. LLM Interaction and AI Services

These components facilitate communication with the core AI models and related services.

| Category | Technology | Type | Purpose |
| :--- | :--- | :--- | :--- |
| **Client** | `openai` | Python Library | Client for interacting with the configured LLM API. |
| **API** | **OpenAI-compatible LLM API** | External Service | Core intelligence and decision-making layer. |
| **Utility** | `manus-speech-to-text` (Utility) | Custom Utility | Transcribes audio/video files using an underlying API (e.g., Whisper). |
| **Protocol** | **Model Context Protocol (MCP)** | Internal API | Suggested backbone for managing tools, resources, and prompts (`manus-mcp-cli`). |

## 4. Cloud and Persistence

Technologies used for external storage, cloud interaction, and data persistence.

| Category | Technology | Type | Purpose |
| :--- | :--- | :--- | :--- |
| **Cloud SDK** | `boto3` | Python Library | AWS SDK for Python, used for interacting with services like S3. |
| **Cloud SDK** | `botocore` | Python Library | Low-level interface to AWS services (dependency of `boto3`). |
| **Storage** | **S3-compatible Object Storage** | External Service | Persistent storage for files and assets. |
| **Utility** | `manus-upload-file` (Utility) | Custom Utility | Uploads files to S3 and returns a public URL. |
| **Database** | **SQLite** | Implicit | File-based database for local data persistence (via Python's standard library). |

## 5. Document and Media Processing

Libraries and utilities for handling file formats, content generation, and transformation.

| Category | Technology | Type | Purpose |
| :--- | :--- | :--- | :--- |
| **PDF/HTML** | `weasyprint` | Python Library | HTML/CSS to PDF converter. |
| **PDF/HTML** | `xhtml2pdf` | Python Library | HTML to PDF converter. |
| **PDF/Doc** | `fpdf2`, `reportlab` | Python Library | Libraries for generating PDF documents programmatically. |
| **Excel** | `openpyxl` | Python Library | Library for reading and writing Excel files. |
| **Markdown** | `markdown` | Python Library | Converts Markdown to HTML. |
| **Utility** | `manus-md-to-pdf` (Utility) | Custom Utility | Converts Markdown files to PDF. |
| **Utility** | `manus-render-diagram` (Utility) | Custom Utility | Renders diagrams (Mermaid, D2, PlantUML) to PNG. |
| **Utility** | `manus-export-slides` (Utility) | Custom Utility | Exports presentation URIs to PDF/PPT. |

## 6. Browser Automation and Web Scraping

Technologies used for interacting with web pages and extracting content.

| Category | Technology | Type | Purpose |
| :--- | :--- | :--- | :--- |
| **Automation** | `playwright` | Python Library | Core library for browser automation. |
| **Engine** | **Chromium** | Browser Engine | The underlying browser used by Playwright. |
| **Scraping** | `beautifulsoup4` | Python Library | Library for pulling data out of HTML and XML files. |
| **Scraping** | `lxml` | Python Library | High-performance XML and HTML processing library. |
| **Scraping** | `cssselect2` | Python Library | CSS selectors for use with lxml/BeautifulSoup. |

## 7. System and Utility

General-purpose tools for environment management and core operations.

| Category | Technology | Type | Purpose |
| :--- | :--- | :--- | :--- |
| **Package Manager** | `pnpm` | Node.js Tool | Fast, disk-space efficient package manager. |
| **Package Manager** | `npm` | Node.js Tool | Default Node.js package manager. |
| **Templating** | `jinja2` | Python Library | Fast, expressive, extensible templating engine. |
| **Validation** | `pydantic` | Python Library | Data validation and settings management using Python type hints. |
| **Utility** | `tqdm` | Python Library | Fast, extensible progress bar for loops. |
