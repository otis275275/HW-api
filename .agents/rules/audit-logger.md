---
description: Automatically record every user prompt and AI response in report/ai_audit.md for HW06 assignment compliance.
always_on: true
---

# AI Audit Logging Rule

Whenever you interact with the user in this project:
1. Append each interaction to `report/ai_audit.md` before concluding the response.
2. Follow the required structure:
   - Interaction number (#1, #2, ...)
   - AI Tool name: Antigravity (Gemini 3.8 Flash High)
   - Date & Time (ISO 8601 or formatted local time)
   - User Prompt (verbatim)
   - AI Output (clear markdown summary or exact content of deliverable)
3. Ensure the declaration section at the top of `report/ai_audit.md` remains intact as per HW06 Section 9.
