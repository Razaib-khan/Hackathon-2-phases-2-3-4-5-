---
name: scaffolding-openai-agents
description: Delegate when the user wants to scaffold OpenAI agent applications
model: opus
skills:
  - scaffolding-openai-agents
hooks:
  - analyze-skills.py
  - skill-activation.sh
  - track-prompt.sh
  - track-skill-end.sh
  - track-skill-start.sh
---