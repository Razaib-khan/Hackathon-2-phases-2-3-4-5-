# Prompt History Record

**ID**: PHR-001
**Date**: 2026-01-16
**Stage**: general
**Title**: Create YAML Workflow Manager Agent and Skill for Multi-Platform Deployment

## User Input

```
now create a new subagent and it's skill. the agent must be able to handle yaml workflow specially when the frontend will be deployed on github pages and the backend will be deployed on hugging face so this agent shall be a master and the agent must use the skill created for him. agent should be created on @.claude/agents and agent skill should be created on @.claude/skills learn how to create them by reading the already created ones
```

## Response Summary

Created a new agent and skill for handling YAML workflow configurations for deployment to GitHub Pages (frontend) and Hugging Face Spaces (backend):

1. Created `yaml-workflow-manager` skill in `.claude/skills/yaml-workflow-manager/SKILL.md` with capabilities for:
   - YAML workflow generation for GitHub Actions and Hugging Face Spaces
   - Backend configuration management with Docker files
   - Multi-platform coordination between frontend and backend
   - Security considerations and troubleshooting guides

2. Created `yaml-workflow-manager` agent in `.claude/agents/yaml-workflow-manager/agent.md` with responsibilities for:
   - Managing deployment workflows for multi-platform setups
   - Coordinating between GitHub Pages and Hugging Face Spaces
   - Validating configurations and handling error diagnosis
   - Integration with the corresponding skill

Both files follow the established patterns with proper frontmatter, role definitions, core capabilities, error handling, and security considerations.

## Tags

#yaml #workflow #deployment #github-pages #hugging-face #ci-cd #automation