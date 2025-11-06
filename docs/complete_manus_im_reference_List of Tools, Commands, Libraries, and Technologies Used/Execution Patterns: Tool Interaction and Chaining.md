# Execution Patterns: Tool Interaction and Chaining

This document analyzes the execution patterns and "relaying features" that define the agent's complex workflows, focusing on the chaining of tool outputs to inputs.

## 1. The Core Orchestration Loop

The agent's execution is a continuous loop orchestrated by the LLM, which uses the `plan` tool to manage state.

| Tool | Role in Orchestration | Key Instruction |
| :--- | :--- | :--- |
| **`plan`** | State Management | Ensures sequential, goal-oriented execution. |
| **`message`** | Feedback Loop | Pauses execution for user input (`ask`) or terminates with results (`result`). |
| **`shell`** | Action Execution | Executes low-level commands, often to start a process that another tool will interact with (e.g., starting a server for `expose`). |
| **`file`** | Data Flow | Acts as the central hub for all data transfer between tools and processes. |

## 2. Key Execution Chains (Relaying Features)

### A. Web Service Deployment Chain

This chain demonstrates the agent's ability to deploy and test its own code.

1.  **Code Execution**: `shell:exec` (e.g., `uvicorn app:app --port 8000`)
2.  **Public Exposure**: `expose:port` (8000) $\rightarrow$ Returns `https://...manusvm.computer`
3.  **Verification**: `browser:url` (Public URL) $\rightarrow$ `browser:informational` or `transactional` intent to test the service.

### B. Research and Data Extraction Chain

This chain highlights the integration of external search with local automation.

1.  **Discovery**: `search:info` $\rightarrow$ Returns list of URLs.
2.  **Navigation**: `browser:url` (URL from search) $\rightarrow$ `browser:informational` (with `focus` parameter).
3.  **Extraction**: `browser` (internal tools) $\rightarrow$ Returns extracted text/data.
4.  **Persistence**: `file:write` or `file:append` (Extracted data) $\rightarrow$ Saves to local file.
5.  **Analysis**: `shell:exec` (Python script using `pandas` or `beautifulsoup4`) $\rightarrow$ Processes the local file.

### C. Media and Document Production Chain

This chain shows the transformation of raw content into final deliverables.

1.  **Content Creation**: `file:write` (Markdown content outline).
2.  **Presentation Generation**: `slides:slide_content_file_path` (Path to Markdown file) $\rightarrow$ Returns `manus-slides://URI`.
3.  **Final Export**: `manus-export-slides` (Utility) $\rightarrow$ Takes URI and outputs final PDF/PPT file.

## 3. Browser Automation Capabilities

The `browser` tool, powered by Playwright, is designed for high-fidelity interaction.

*   **Login Persistence**: The browser maintains login state across tasks, eliminating the need for repeated authentication.
*   **Intent-Driven Interaction**: The `intent` parameter (`navigational`, `informational`, `transactional`) dictates the agent's internal strategy for interacting with the page, optimizing for reading vs. performing actions.
*   **User Takeover**: The `message:ask` with `take_over_browser` is the explicit mechanism for handling CAPTCHAs, 2FA, or other manual steps, ensuring the agent does not attempt to bypass security measures.
