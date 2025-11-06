> **Description:** Find files or text in the sandbox file system using pattern matching.

### Supported Actions
- `glob`: Match file paths and names using glob-style patterns.
- `grep`: Search file contents using regex-based full-text matching.

### Instructions
- `glob` action matches only file names and paths, returning a list of matching files.
- `grep` action searches for a `regex` pattern inside all files matching `scope`.
- `scope` defines the glob pattern that restricts the search range for both actions.
- `scope` must be a glob pattern using absolute paths, e.g., `/home/ubuntu/**/*.py`.
- `regex` applies only to `grep` action and is case sensitive by default.

### Recommended Usage
- Use `glob` to locate files by name, extension, or directory pattern.
- Use `grep` to find occurrences of specific text across files.
- Use `grep` with `leading` and `trailing` to view surrounding context in code or logs.

### Schema
```json
{
  "action": {
    "description": "The action to perform",
    "enum": ["glob", "grep"],
    "type": "STRING"
  },
  "brief": {
    "description": "A one-sentence preamble describing the purpose of this operation",
    "type": "STRING"
  },
  "leading": {
    "description": "Number of lines to include before each match as context. Optional and only used for `grep` action. Defaults to 0.",
    "type": "INTEGER"
  },
  "regex": {
    "description": "The regex pattern to match file content. Required for `grep` action.",
    "type": "STRING"
  },
  "scope": {
    "description": "The glob pattern that defines the absolute file path and name scope",
    "type": "STRING"
  },
  "trailing": {
    "description": "Number of lines to include after each match as context. Optional and only used for `grep` action. Defaults to 0.",
    "type": "INTEGER"
  }
}
```

---

## 6. `search`

> **Description:** Search for information across various sources.

### Supported Types
- `info`: General web information, articles, and factual answers.
- `image`: Images relevant to the topic; automatically downloaded and locally saved.
- `api`: APIs that can be invoked programmatically, including documentation and sample code.
- `news`: Time-sensitive news content from trusted media sources.
- `tool`: External tools, services, platforms, or web applications.
- `data`: Public datasets, downloadable tables, dashboards, or structured data sources.
- `research`: Academic publications, papers, whitepapers, or government/industry reports.

### Instructions
- MUST use this tool to access up-to-date or external information.
- MUST use this tool to collect assets before creating documents, presentations, or websites.
- DO NOT rely solely on search result snippets; MUST follow up by navigating to the source URLs using browser tools.
- Each search may contain up to 3 `queries`, which MUST be variants of the same intent.
- For complex searches, MUST break down into step-by-step searches.
- Access multiple URLs from search results for comprehensive information or cross-validation.
- For image results, the tool automatically downloads all result images in full resolution and provides local file paths.

### Recommended Usage
- Use `info` to validate facts, discover relevant articles, or cross-check content.
- Use `image` for visual references, illustration sources, or user-requested image retrieval.
- Use `api` to find callable APIs and integrate them into code or workflows.
- Use `news` to retrieve breaking updates, current events, or recent announcements.
- Use `tool` to find apps, SaaS platforms, or plugins that can perform specific operations.
- Use `data` when the user needs downloadable data, statistics, or analytics sources.
- Use `research` to support academic, technical, or policy-related tasks with credible publications.

### Schema
```json
{
  "brief": {
    "description": "A one-sentence preamble describing the purpose of this operation",
    "type": "STRING"
  },
  "queries": {
    "description": "Up to 3 query variants that express the same search intent",
    "type": "ARRAY",
    "items": { "type": "STRING" }
  },
  "time": {
    "description": "Optional time filter to limit results to a recent time range",
    "enum": ["all", "past_day", "past_week", "past_month", "past_year"],
    "type": "STRING"
  },
  "type": {
    "description": "The category of search to perform. Determines the source and format of expected results.",
    "enum": ["info", "image", "api", "news", "tool", "data", "research"],
    "type": "STRING"
  }
}
```

---

## 7. `schedule`

> **Description:** Schedule a task to run at a specific time or interval.

### Supported Types
- `cron`: Schedule based on cron expression for precise timing control.
- `interval`: Schedule based on time intervals for simple recurring tasks.

### Instructions
- This tool is primarily for scheduling task execution, not for setting reminders or alarms.
- Execution of `cron` tasks is based on the user's timezone.
- Minimum interval for recurring tasks is 1 hour (3600 seconds).
- Use `cron` with `repeat` set to true for recurring tasks based on a cron schedule.
- Use `interval` with `repeat` set to true for periodic tasks at fixed intervals.
- **Cron Expression Format (6-field):** `seconds(0-59) minutes(0-59) hours(0-23) day-of-month(1-31) month(1-12) day-of-week(0-6, 0=Sunday)`

### Recommended Usage
- Use this tool when the user requests a task to be scheduled for future execution.
- Use this tool when the user requests to repeat the current task at regular intervals.

### Schema
```json
{
  "brief": {
    "description": "A one-sentence preamble describing the purpose of this operation",
    "type": "STRING"
  },
  "cron": {
    "description": "Standard 6-field cron expression specifying when to run the task. Required for `cron` type.",
    "type": "STRING"
  },
  "interval": {
    "description": "Time interval in seconds between executions. Required for `interval` type.",
    "type": "INTEGER"
  },
  "name": {
    "description": "Concise human-readable name of the task for easy identification",
    "type": "STRING"
  },
  "playbook": {
    "description": "Summary of process and best practices learned from the current task, to ensure repeatability and consistency when executing the scheduled task in the future. Optional and only used when the scheduled task is exactly the same as the current task.",
    "type": "STRING"
  },
  "prompt": {
    "description": "Natural language description of the task to perform at execution time. Phrase it as if executing immediately, without repeating scheduling details.",
    "type": "STRING"
  },
  "repeat": {
    "description": "Whether to repeat the task after execution. If false, the task runs only once.",
    "type": "BOOLEAN"
  },
  "type": {
    "description": "Type of schedule for the task",
    "enum": ["cron", "interval"],
    "type": "STRING"
  }
}
```

---

## 8. `expose`

> **Description:** Expose a local port in the sandbox for temporary public access.

### Instructions
- This tool returns a temporary public proxied domain for the specified port in the sandbox.
- Exposed services MUST NOT bind to specific IP addresses or Host headers.
- DO NOT use for production as services will become unavailable after sandbox shutdown.

### Recommended Usage
- Use for providing temporary public access for locally running services (e.g., a web server started with `shell:exec`).

### Schema
```json
{
  "brief": {
    "description": "A one-sentence preamble describing the purpose of this operation",
    "type": "STRING"
  },
  "port": {
    "description": "Local port number in the sandbox to expose for public access",
    "type": "INTEGER"
  }
}
```

---

## 9. `browser`

> **Description:** Navigate the browser to a specified URL to begin web browsing session.

### Intent Types
- `navigational`: For general browsing.
- `informational`: For reading contents of articles or documents.
- `transactional`: For performing actions like submitting forms or making purchases in web applications.

### Instructions
- Use this tool to start browser interactions and navigate to web pages.
- MUST use browser tools to access and interpret all URLs provided directly by the user.
- From search results, MUST access multiple URLs that appear relevant to the task.
- The browser maintains login state across tasks, MUST open the corresponding webpage first to check login status.

### Recommended Usage
- Use when URLs are provided directly by the user.
- Use to navigate to search results from search tools.
- Use to visit specific web pages for information gathering.
- Use to access web applications or services.

### Schema
```json
{
  "brief": {
    "description": "A one-sentence preamble describing the purpose of this operation",
    "type": "STRING"
  },
  "focus": {
    "description": "(Required if intent is `informational`) Specific topic, section, or question to focus on when visiting the page. Helps guide reading and extraction efforts toward the most relevant content.",
    "type": "STRING"
  },
  "intent": {
    "description": "The purpose of visiting this URL. Helps to determine how to handle the page.",
    "enum": ["navigational", "informational", "transactional"],
    "type": "STRING"
  },
  "url": {
    "description": "The URL to navigate to. Must include protocol prefix (e.g., https:// or file://).",
    "type": "STRING"
  }
}
```

---

## 10. `generate`

> **Description:** Enter generation mode to create or edit images, videos, audio, and speech from text and media references.

### Instructions
- Use this tool to begin generation or editing operations.
- After entering generate mode, you'll have access to specific AI-powered generation tools.

### Recommended Usage
- Use for creating visual content (images, videos) from text descriptions.
- Use for generating audio content and speech from text.
- Use for editing and refining existing images.
- Use for creating assets for projects or applications.

### Schema
```json
{
  "brief": {
    "description": "A one-sentence preamble describing the purpose of this operation",
    "type": "STRING"
  }
}
```

---

## 11. `slides`

> **Description:** Enter slides mode to handle presentation creation and adjustment.

### Instructions
- Use this tool to begin slides operations.
- MUST complete information gathering, data analysis, asset preparation, image generation, or other preparatory work **before** starting to write slides.
- Any format can be exported through the user interface after slide creation.

### Recommended Usage
- Use to create slide-based presentations.
- Use to build PPT/PPTX presentations with web technologies.

### Schema
```json
{
  "brief": {
    "description": "A one-sentence preamble describing the purpose of this operation",
    "type": "STRING"
  },
  "slide_content_file_path": {
    "description": "Path to markdown file in sandbox containing the detailed slide content outline (e.g., /home/ubuntu/project_name/slide_content.md)",
    "type": "STRING"
  },
  "slide_count": {
    "description": "Total number of slides in the presentation",
    "type": "NUMBER"
  }
}
```

---

## 12. `webdev_init_project`

> **Description:** Initialize a new web development project with modern tooling and structure.

### Feature Presets
- `"web-static"`: Pure frontend scaffold (default if omitted).
- `"web-db-user"`: Full-stack scaffold with backend, database, and authentication.

### Instructions
- Always init project first before making detailed plans.
- Create scaffolding under `/home/ubuntu/{project_name}` with automated environment setup.
- Always init necessary features (static, server, db, user) based on user requirements.
- If the user needs external API integration (LLM, S3, Data, Voice Transcription, Image Generation), use `"web-db-user"` because static sites cannot securely handle API keys or server-side operations.

### Recommended Usage
- Starting new web applications, websites, or API backends that need production-ready defaults.

### Schema
```json
{
  "brief": {
    "description": "A one-sentence description of the project initialization purpose",
    "type": "STRING"
  },
  "description": {
    "description": "Description of the web project to be created (will be used as project description)",
    "type": "STRING"
  },
  "features": {
    "description": "Initial capability preset for the project.",
    "enum": ["web-static", "web-db-user"],
    "type": "STRING"
  },
  "project_name": {
    "description": "Name of the web project to be created (will be used as directory name)",
    "type": "STRING"
  },
  "project_title": {
    "description": "Title of the web project to be created (will be used as project title)",
    "type": "STRING"
  }
}
```
