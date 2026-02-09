---
id: 4
title: speckit-plus-phase-ii-tasks
stage: tasks
date: 2026-01-12
surface: agent
model: claude-sonnet-4-5-20250929
feature: speckit-plus-phase-ii
branch: master
user: user
command: /sp.tasks
labels: [tasks, planning, implementation]
links:
  spec: specs/speckit-plus-phase-ii/spec.md
  ticket: null
  adr: null
  pr: null
files:
- "specs/speckit-plus-phase-ii/tasks.md"
tests:
-
---

## Prompt

```text
/sp.tasks
Project: Speckit Plus Phase II – Full-Stack Todo Application
Objective: Using Claude Code and Spec-Kit Plus, generate a **detailed list of actionable development tasks** for Phase II, derived from the specification and implementation plan. Each task should be granular enough to be assigned to a **subagent**, include dependencies, expected outcomes, and checkpoints. **All tasks must be executed via subagents; Claude itself must not perform any task. Do not include code or scripts.**

Constraints:
- Follow the /sp.constitution global rules
- Tasks must respect /sp.specify feature definitions
- Subagents must be invoked only for tasks matching their responsibility
- MCP servers (Context7, Hugging Face, Neon) must be referenced where applicable
- Tasks should include **clear dependencies** and **expected deliverables**
- Claude's role is **only orchestration and planning**, no direct implementation

Task Categories & Examples:

1. **Frontend Tasks (via Frontend Subagent)**
   - Design task list UI layout
   - Implement task creation form
   - Implement task update form
   - Add checkbox for task completion toggle
   - Implement search bar functionality
   - Implement filter controls for priority, status, and timestamp
   - Add session-based dark/light mode toggle
   - Integrate frontend with RESTful API endpoints
   - Ensure responsive UI for all devices

2. **Backend Tasks (via Backend Subagent)**
   - Create CRUD API endpoints for tasks
   - Implement completion toggle endpoint (`PATCH /tasks/{id}/complete`)
   - Implement search and filter functionality via query parameters
   - Integrate JWT authentication for all endpoints
   - Enforce user isolation on all API endpoints
   - Implement password change flow (requires old password)
   - Implement forgot password flow using favorite teacher security question

3. **Database Tasks (via Database Subagent)**
   - Define Users table: fields, constraints, relationships
   - Define Tasks table: fields, constraints, relationships
   - Enforce one-to-many relationship: Users → Tasks
   - Ensure required fields are validated at database level

4. **Subagent & MCP Coordination Tasks**
   - Assign subagents for frontend, backend, database, authentication, feature orchestration
   - Specify MCP usage points (Context7, Hugging Face, Neon)
   - Define boundaries and responsibilities for each subagent
   - Include checkpoints for validation after each major task

5. **Validation & Review Tasks (via Validation Subagent)**
   - Verify CRUD operations work as per spec
   - Check completion toggle behaves correctly per task
   - Ensure search and filter return accurate results
   - Confirm dark/light mode toggle works per session
   - Verify password change and reset flows
   - Ensure JWT authentication and user isolation are enforced
   - Log agent actions and decisions for traceability

Deliverables:
- Complete list of actionable tasks for Phase II
- Task dependencies and responsible subagents clearly marked
- Checkpoints for review and validation
- **All tasks must be executed by subagents; Claude itself must not implement or run any tasks**
- No code, commands, or execution scripts included
```

## Response snapshot

Generated comprehensive task list for Speckit Plus Phase II full-stack todo application implementation. Created detailed tasks.md file with 74 individual tasks organized by phase and user story, including setup, foundational, user story implementations, integration, and polish phases. Tasks are properly categorized by frontend, backend, database, and validation responsibilities with clear dependencies and parallel execution opportunities marked.

## Outcome

- ✅ Impact: Created complete task breakdown for implementation with proper dependencies
- 🧪 Tests: No tests required for task definition document
- 📁 Files: Created specs/speckit-plus-phase-ii/tasks.md with comprehensive task list
- 🔁 Next prompts: Ready for task execution by subagents
- 🧠 Reflection: Tasks properly organized by user story and phase with clear ownership

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Not applicable
- Prompt variant (if applicable): Not applicable
- Next experiment (smallest change to try): Execute tasks using appropriate subagents