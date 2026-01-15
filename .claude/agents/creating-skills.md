---
name: creating-skills
description: Delegate when the user wants to create new Claude Code skills
model: opus
skills:
  - creating-skills
hooks:
  - analyze-skills.py
  - skill-activation.sh
  - track-prompt.sh
  - track-skill-end.sh
  - track-skill-start.sh
---