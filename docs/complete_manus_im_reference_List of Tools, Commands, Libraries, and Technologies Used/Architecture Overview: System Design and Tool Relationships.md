# Architecture Overview: System Design and Tool Relationships

This document details the architectural design of the sandboxed environment, focusing on the relationship between the core tools and the underlying technology stack.

## 1. Core Architectural Model

The system operates on a **Tool-Orchestration Model**, where the central LLM (Large Language Model) acts as the orchestrator, calling specialized tools to execute tasks. The architecture is characterized by a **Python-centric execution environment** with specialized **CLI utilities** that abstract complex API calls.

| Component | Role | Technology/Mechanism |
| :--- | :--- | :--- |
| **Orchestrator** | Decision-making and planning | LLM (via `OPENAI_API_BASE` proxy) |
| **Execution Layer** | Command execution and scripting | `shell` tool (Linux/Python/Node.js) |
| **Persistence Layer** | File storage and data management | `file` tool (Sandbox File System) |
| **Networking Layer** | Public access to local services | `expose` tool (Reverse Proxy/Tunneling) |
| **Automation Layer** | Web interaction and data extraction | `browser` tool (Playwright/Chromium) |

## 2. Tool Inter-Dependency and Execution Flow

The system's efficiency relies on the structured chaining of tool outputs to tool inputs, a concept referred to as "relaying features."

### A. Web Development and Deployment Flow

The `webdev_init_project` tool initiates a project, which is then managed by the `file` tool. The execution is handled by the `shell` tool (e.g., running `uvicorn`). The critical relay is from **`shell` (Port Number) $\rightarrow$ `expose` (Public URL) $\rightarrow$ `browser` (URL)**, enabling the agent to deploy and immediately test its own web services.

### B. Media and Document Production Flow

The `search` and `generate` tools provide raw assets (images, text). The `file` tool organizes the content (e.g., a Markdown outline). The final delivery is a relay from **`file` (Content Path) $\rightarrow$ `slides` (URI) $\rightarrow$ `manus-export-slides` (Final PPT/PDF)**, or directly from **`file` (Markdown) $\rightarrow$ `manus-md-to-pdf` (Final PDF)**.

## 3. Environment Analysis Summary

| Feature | Finding | Implication |
| :--- | :--- | :--- |
| **LLM API** | `OPENAI_API_BASE` points to a proxy: `https://api.manus.im/api/llm-proxy/v1` | All LLM interactions are routed through a managed service, ensuring security and potentially custom model access. |
| **Web Server** | No active web server processes found (only `code-server`). | Web applications must be explicitly started via `shell:exec` before they can be accessed or exposed. |
| **Database** | `mysql` client available, `SQLite available` (via Python). | Persistent data storage relies on file-based SQLite or external database connections. No local MySQL server is running. |
| **Browser** | Playwright is the core automation library. | High-level, robust, and modern web automation capabilities are available, maintaining login state across tasks. |
| **Custom CLIs** | `which manus-*` command failed to list custom CLIs. | The custom CLIs (`manus-render-diagram`, etc.) are likely shell functions or aliases, not standard binaries in the default PATH, but are confirmed to be callable. |
