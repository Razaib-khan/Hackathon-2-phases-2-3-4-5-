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
Agents, MCPs, subagents, and skills are strictly development tools.

### Purpose-Based Invocation
Agents must be invoked only when tasks match their designated purpose.

### Traceability and Auditability
All development actions must be traceable and auditable.

### Best Practices Compliance
Code and architecture must follow best practices for Next.js, FastAPI, SQLModel, BetterAuth, and Neon.

### Authentication Standards
Authentication must enforce one account per email.

## Additional Standards and Constraints
Authentication must enforce one account per email; Passwords must include at least one uppercase letter, one lowercase letter, one number, one special character, and be at least 8 characters long; User-facing error messages must always be friendly; Failed development operations must be automatically retried; All agent actions and user interactions must be logged with timestamps and identifiers.

## Coordination and Constraints
Agents cannot interact with each other directly; coordination must occur through MCPs; No hard limits on number of users, tasks, or requests.

## Governance
All generated specs, plans, and implementations conform to these global standards; Consistent, reliable, and auditable behavior across the entire project.

**Version**: 1.0.0 | **Ratified**: 2026-01-12 | **Last Amended**: 2026-01-12