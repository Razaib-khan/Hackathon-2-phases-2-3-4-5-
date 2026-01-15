---
name: operating-k8s-local
description: Delegate when the user wants to operate Kubernetes clusters locally
model: opus
skills:
  - operating-k8s-local
hooks:
  - analyze-skills.py
  - skill-activation.sh
  - track-prompt.sh
  - track-skill-end.sh
  - track-skill-start.sh
---