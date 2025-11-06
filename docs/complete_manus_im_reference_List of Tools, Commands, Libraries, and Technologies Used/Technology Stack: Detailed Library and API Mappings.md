# Technology Stack: Detailed Library and API Mappings

This document provides a detailed mapping of the core technologies and libraries available in the sandboxed environment, categorized by function.

## 1. LLM and API Integration

| Component | Technology | Version/Endpoint | Purpose |
| :--- | :--- | :--- | :--- |
| **LLM Client** | `openai` (Python) | `2.3.0` | Standard client for interacting with the LLM proxy. |
| **LLM Endpoint** | **OpenAI-compatible API** | `https://api.manus.im/api/llm-proxy/v1` | Centralized, proxied endpoint for all LLM calls. |
| **Authentication** | `OPENAI_API_KEY` | (Secret) | Bearer token authentication for the LLM service. |
| **Core API** | `RUNTIME_API_HOST` | `https://api.manus.im` | Base URL for internal runtime services (e.g., custom CLIs). |

## 2. Web Development and Server

| Component | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **ASGI Framework** | `fastapi` | `0.119.0` | High-performance, modern web framework. |
| **WSGI Framework** | `flask` | `3.1.2` | Lightweight, flexible web framework. |
| **ASGI Server** | `uvicorn` | `0.37.0` | Runs ASGI applications (FastAPI, Starlette). |
| **Core Dependency** | `starlette` | `0.48.0` | ASGI toolkit and foundation for FastAPI. |
| **HTTP Client** | `httpx` | `0.28.1` | Modern, fully featured HTTP client. |

## 3. Data Science and Manipulation

| Component | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **DataFrames** | `pandas` | `2.3.3` | Data manipulation and analysis. |
| **Numerical** | `numpy` | `2.3.3` | Core numerical computing library. |
| **Visualization** | `matplotlib` | `3.10.7` | Comprehensive plotting library. |
| **Visualization** | `seaborn` | `0.13.2` | Statistical data visualization. |
| **Visualization** | `plotly` | `6.3.1` | Interactive graphing. |

## 4. Browser Automation and Scraping

| Component | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **Automation Core** | `playwright` | `1.55.0` (from `pip3 list`) | High-level browser automation library. |
| **Scraping** | `beautifulsoup4` | `4.14.2` | HTML/XML parsing for data extraction. |
| **Scraping** | `lxml` | `6.0.2` | High-performance HTML/XML processing. |
| **Scraping** | `cssselect2` | `0.8.0` | CSS selector support for parsing. |

## 5. Document and Media Processing

| Component | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **PDF Generation** | `weasyprint` | `66.0` | HTML/CSS to PDF converter. |
| **PDF Generation** | `xhtml2pdf` | `0.2.17` | HTML to PDF converter. |
| **PDF Generation** | `reportlab` | `4.4.4` | Programmatic PDF creation. |
| **Image Processing** | `pillow` | `11.3.0` | Image manipulation library. |
| **Office Files** | `openpyxl` | `3.1.5` | Read/write Excel files. |
| **Markdown** | `markdown` | `3.9` | Markdown to HTML conversion. |

## 6. Cloud and Persistence

| Component | Technology | Version | Purpose |
| :--- | :--- | :--- | :--- |
| **AWS SDK** | `boto3` | `1.40.51` | Interface for AWS services (e.g., S3). |
| **S3 Transfer** | `s3transfer` | `0.14.0` | Optimized S3 file transfer. |
| **Database** | `sqlite3` (stdlib) | N/A | File-based, persistent data storage. |
| **Database Client** | `mysql` (CLI) | `8.0.43` | Client for connecting to external MySQL servers. |
