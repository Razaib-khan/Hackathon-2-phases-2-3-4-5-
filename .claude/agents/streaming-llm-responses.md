---
name: streaming-llm-responses
description: Delegate when the user wants to implement streaming responses from LLMs
model: opus
skills:
  - streaming-llm-responses
hooks:
  - analyze-skills.py
  - skill-activation.sh
  - track-prompt.sh
  - track-skill-end.sh
  - track-skill-start.sh
---