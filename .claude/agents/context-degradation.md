---
name: context-degradation
description: Delegate when the user wants to recognize, diagnose, and mitigate patterns of context degradation in agent systems
model: opus
skills:
  - context-degradation
hooks:
  - analyze-skills.py
  - skill-activation.sh
  - track-prompt.sh
  - track-skill-end.sh
  - track-skill-start.sh
---