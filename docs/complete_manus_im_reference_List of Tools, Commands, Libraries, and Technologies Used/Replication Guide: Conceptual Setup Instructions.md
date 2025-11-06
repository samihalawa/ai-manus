# Replication Guide: Conceptual Setup Instructions

This guide outlines the conceptual steps required to replicate the core components of the sandboxed environment. Note that the agent operates in a highly pre-configured environment, and this guide serves to document the necessary components rather than provide executable setup scripts.

## 1. Operating System and Base Environment

| Component | Requirement | Setup Command (Conceptual) |
| :--- | :--- | :--- |
| **OS** | Ubuntu 22.04 (or similar Linux distribution) | `sudo apt update && sudo apt upgrade` |
| **Python** | Python 3.11+ | `sudo apt install python3.11 python3-pip` |
| **Node.js** | Node.js 22+ | `curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash - && sudo apt-get install -y nodejs` |
| **MySQL Client** | MySQL Client CLI | `sudo apt install default-mysql-client` |

## 2. Python Environment Setup

The core functionality is provided by a large set of Python packages.

1.  **Install Core Packages**: Install all packages listed in `python_packages.txt`.
    *   **Key Packages**: `fastapi`, `flask`, `uvicorn`, `playwright`, `openai`, `boto3`, `pandas`, `beautifulsoup4`, `weasyprint`.
2.  **Playwright Dependencies**: Install the necessary browser binaries for Playwright.
    *   **Command**: `playwright install chromium` (This is typically handled automatically by the environment).

## 3. API and Authentication Configuration

The environment relies on specific environment variables for API access.

1.  **LLM Configuration**: Set the environment variables for the LLM service.
    *   **Variables**:
        *   `OPENAI_API_KEY`: Your secret API key.
        *   `OPENAI_BASE_URL`: The proxy endpoint (`https://api.manus.im/api/llm-proxy/v1`).
2.  **Cloud Configuration**: Configure access to S3-compatible storage.
    *   **Mechanism**: Typically involves setting `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` (or relying on the `boto3` configuration).

## 4. Custom Tool Integration (Conceptual)

The custom `manus-*` utilities are proprietary wrappers around internal APIs. To replicate their functionality, one would need to:

1.  **Implement Wrappers**: Create Python or shell scripts that mimic the functionality of:
    *   `manus-upload-file`: Uses `boto3` to upload a file to a pre-configured S3 bucket and return the public URL.
    *   `manus-md-to-pdf`: Uses a library like `weasyprint` or `xhtml2pdf` to perform the conversion.
    *   `manus-export-slides`: Requires access to the internal slides generation API.
2.  **Port Exposure**: The `expose` tool requires a reverse proxy/tunneling service (e.g., ngrok, Cloudflare Tunnel) to map a local port to a public URL. This is a complex, external service integration.
