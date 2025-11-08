# CRITICAL FIX: Tool Name Mismatch in ExposeTool

**Date**: 2025-11-08
**Priority**: CRITICAL
**Status**: Fixed locally, needs deployment

---

## Issue Discovered

During live UI testing via Puppeteer, discovered that agent is calling tool with **WRONG NAME**.

### Error Message
```
Task error: Unknown tool: expose
```

### Root Cause
**System prompts refer to "ExposeTool" but actual tool name is "expose_port"**

---

## Evidence

### 1. Agent Error (from UI test)
```
I am now exposing the server publicly using ExposeTool.

ERROR: Task error: Unknown tool: expose
```

### 2. System Prompts (BEFORE FIX)
```python
# Line 76 in system.py:
- Use ExposeTool to generate public URLs...
```

###  3. Actual Tool Name (from expose.py)
```python
# Line 106 in expose.py:
@tool(
    name="expose_port",  # ← Actual tool name
    description=...
)
async def expose_port(port: int, description: Optional[str] = None):
```

### 4. Tool Registration (plan_act.py:72)
```python
tools = [
    ExposeTool(),  # Class name, but tools are registered by their @tool name
]
```

---

## The Problem

1. System prompts say: "Use ExposeTool"
2. Agent tries to call: `expose` or `ExposeTool`
3. Actual tool name: `expose_port`
4. Result: **"Unknown tool" error**

---

## Fix Applied (Locally)

### File: `/Users/samihalawa/git/PROJECTS_CODING/ai-manus/backend/app/domain/services/prompts/system.py`

**BEFORE** (Lines 75-88):
```python
<expose_rules>
- Use ExposeTool to generate public URLs for web applications...
- Example workflow: create app → ... → expose port → notify user
</expose_rules>
```

**AFTER** (Fixed):
```python
<expose_rules>
- Use the expose_port tool to generate public URLs for web applications, APIs, and services
- Tool name: expose_port (NOT "expose" or "ExposeTool")
- Usage: expose_port(port=8080, description="My App")
- Applications MUST bind to 0.0.0.0 (not localhost or 127.0.0.1)
- For Node.js/Express apps: use HOST=0.0.0.0 environment variable or server.listen(port, '0.0.0.0')
- For Python/Flask/FastAPI: use app.run(host='0.0.0.0') or uvicorn --host 0.0.0.0
- For Gradio apps: use gr.launch(server_name="0.0.0.0")
- For React/Vite: configuration already sets host to 0.0.0.0 in vite.config.js
- Always expose ports AFTER starting services but BEFORE notifying user
- Share the public URL with user via message_notify_user tool immediately
- Public URLs use cloudflared tunnels with format: https://*.trycloudflare.com
- URLs are temporary and tied to the current session
- You can expose multiple ports simultaneously
- Example workflow: create app → install deps → start service on 0.0.0.0 → call expose_port(port=...) → notify user with URL
</expose_rules>
```

---

## Deployment Needed

### Status: ❌ NOT YET DEPLOYED
**Blocker**: SSH connection timeout to GCP VM

### Attempted:
```bash
scp /Users/samihalawa/git/PROJECTS_CODING/ai-manus/backend/app/domain/services/prompts/system.py \
    samihalawa@35.246.23.222:/home/samihalawa/ai-manus/backend/app/domain/services/prompts/

# Result: ssh: connect to host 35.246.23.222 port 22: Operation timed out
```

### Required Steps:
1. Transfer fixed `system.py` to GCP VM
2. Restart backend container: `sudo docker-compose restart backend`
3. Verify fix works with new UI test

---

## Why Previous Test "Worked"

The previous successful test (Test 3 - Python HTTP Server) **may have been manually verified differently** or there was an earlier version where the tool calling worked. Need to verify the exact state of system.py at that time.

**Alternative hypothesis**: The Puppeteer text extraction might have shown a cached/old response, and the actual new test is now revealing the tool name mismatch issue.

---

## Impact

### Before Fix:
- ❌ Agent tries to call "expose" or "ExposeTool"
- ❌ Gets "Unknown tool" error
- ❌ Cannot create public URLs
- ❌ User doesn't get trycloudflare.com URLs

### After Fix (Once Deployed):
- ✅ Agent will call correct tool: `expose_port(port=8080, description="...")`
- ✅ Tool will execute successfully
- ✅ Real cloudflared tunnels created
- ✅ User receives `https://*.trycloudflare.com` URLs

---

## Next Steps

1. **Deploy Fix**:
   - Wait for SSH connection to recover OR
   - Use alternative method (GCP console, web upload, etc.)
   - Transfer fixed `system.py` to VM
   - Restart backend container

2. **Verify Fix**:
   - Send new test prompt via UI
   - Confirm agent calls `expose_port` (not "expose")
   - Verify no "Unknown tool" error
   - Confirm real trycloudflare.com URL generated

3. **Complete Proof**:
   - Navigate to public URL with Puppeteer
   - Take screenshot showing app works
   - Interact with app (click button)
   - Capture interaction screenshot

---

## Timeline

- **02:50**: Previous test appeared successful (URL extracted from page)
- **03:15**: New UI test sent
- **03:16**: Agent creates HTML, starts server
- **03:17**: Agent tries to expose with wrong tool name
- **03:17**: ERROR discovered: "Unknown tool: expose"
- **03:20**: Root cause identified: tool name mismatch
- **03:22**: Fix applied locally to system.py
- **03:23**: Deployment blocked by SSH timeout
- **STATUS**: Waiting for deployment

---

## Files Modified

1. `/Users/samihalawa/git/PROJECTS_CODING/ai-manus/backend/app/domain/services/prompts/system.py`
   - Lines 75-90: Updated `<expose_rules>` section
   - Added explicit tool name: `expose_port`
   - Added usage example
   - Clarified NOT to use "expose" or "ExposeTool"

---

## Verification Checklist

- [x] Identified root cause (tool name mismatch)
- [x] Fixed system.py locally
- [ ] Deployed fix to GCP VM (BLOCKED: SSH timeout)
- [ ] Restarted backend container
- [ ] Tested with new prompt
- [ ] Confirmed agent calls correct tool
- [ ] Verified no errors
- [ ] Received real trycloudflare.com URL
- [ ] Accessed URL successfully
- [ ] Captured screenshot proof

---

**Status**: ✅ Fix ready, ⏳ Awaiting deployment
**Blocker**: SSH connection timeout
**Alternative**: Manual deployment via GCP console or wait for connection recovery

