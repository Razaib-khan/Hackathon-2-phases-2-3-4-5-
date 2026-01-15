---
name: import-error-solver
description: Delegate when the user encounters import/export errors in TypeScript/JavaScript modules
model: opus
skills:
  - import-error-resolution
hooks:
  - analyze-import-errors.py
  - resolve-imports.sh
  - track-prompt.sh
  - track-skill-end.sh
  - track-skill-start.sh
---
