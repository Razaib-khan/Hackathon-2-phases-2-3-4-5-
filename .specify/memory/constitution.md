<!--
Sync Impact Report:
- Version change: undefined → 1.0.0
- Modified principles:
  - Immutable Global Standards: Immutable global standards apply to all development and system behavior
  - Development Tools Governance: Agents, MCPs, subagents, and skills are strictly development tools
  - Purpose-Based Invocation: Agents must be invoked only when tasks match their designated purpose
  - Traceability and Auditability: All development actions must be traceable and auditable
  - Best Practices Compliance: Code and architecture must follow best practices for Next.js, FastAPI, SQLModel, BetterAuth, and Neon
  - Authentication Standards: Authentication must enforce one account per email
- Added sections: Additional Standards and Constraints, Coordination and Constraints, Governance
- Removed sections: None
- Templates requiring updates:
  - .specify/templates/plan-template.md: Constitution Check section needs to reflect new constitution principles (TODO: manual update)
  - .specify/templates/spec-template.md: May need alignment with new constraints (TODO: manual review)
  - .specify/templates/tasks-template.md: May need alignment with new principles (TODO: manual review)
  - .specify/templates/phr-template.prompt.md: No changes needed
- Follow-up TODOs: None
-->
# AIDO TODO Application Constitution

## Core Principles

### Immutable Global Standards
Immutable global standards apply to all development and system behavior.

### Development Tools Governance
Agents, MCPs, subagents, and skills are strictly development tools. All implementations must enforce subagent-first, skill-first, and MCP-first execution policies. Enforcement hooks must be triggered for all development operations to ensure compliance with required patterns.

### Purpose-Based Invocation
Agents must be invoked only when tasks match their designated purpose.

### Traceability and Auditability
All development actions must be traceable and auditable. Skill activation and subagent assignment must be tracked through machine-readable artifacts to ensure proper accountability and audit trails.

### Best Practices Compliance
Code and architecture must follow best practices for Next.js, FastAPI, SQLModel, BetterAuth, and Neon.

### Authentication Standards
Authentication must enforce one account per email.

### Mandatory Enforcement Standards
All /sp.implement actions must undergo mandatory validation through enforcement hooks that verify: subagent assignment, skill activation, and MCP tool usage. Implementation will be aborted if any compliance check fails. Hooks ensure that all required artifacts exist and are properly configured before execution proceeds.

### MCP-First Execution Policy
All backend operations during implementation must utilize MCP tools rather than direct database/ORM calls. Plans must include MCP_CALL markers to demonstrate proper tool usage. Direct database operations are prohibited during /sp.implement execution.

## Additional Standards and Constraints
Authentication must enforce one account per email; Passwords must include at least one uppercase letter, one lowercase letter, one number, one special character, and be at least 8 characters long; User-facing error messages must always be friendly; Failed development operations must be automatically retried; All agent actions and user interactions must be logged with timestamps and identifiers; All implementations must pass through enforcement validation before execution.

## Coordination and Constraints
Agents cannot interact with each other directly; coordination must occur through MCPs; No hard limits on number of users, tasks, or requests; Enforcement hooks must validate all implementation prerequisites before proceeding; Subagent-first and skill-first policies must be enforced for all development tasks.

## Governance
All generated specs, plans, and implementations conform to these global standards; Consistent, reliable, and auditable behavior across the entire project; Enforcement systems ensure compliance with subagent-first, skill-first, and MCP-first policies.

**Version**: 1.1.0 | **Ratified**: 2026-01-21 | **Last Amended**: 2026-01-21