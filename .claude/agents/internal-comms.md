---
name: internal-comms
description: Delegate when the user wants to create internal communications like status reports, leadership updates, etc.
model: opus
skills:
  - internal-comms
hooks:
  - analyze-skills.py
  - skill-activation.sh
  - track-prompt.sh
  - track-skill-end.sh
  - track-skill-start.sh
---