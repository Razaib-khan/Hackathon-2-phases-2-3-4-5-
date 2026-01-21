# Enforcement System Documentation

This document describes the enforcement system that ensures Claude cannot bypass subagents, skills, or MCP usage during implementation.

## Overview

The enforcement system provides mandatory checks that prevent Claude from directly implementing tasks without using the required subagents, skills, and MCP tools. The system operates through a series of validation hooks that must pass before any implementation can proceed.

## Components

### 1. Hook Scripts
- `pre-implement-enforce-subagents.sh`: Validates subagent assignment and skill activation
- `pre-mcp-enforce.sh`: Ensures MCP tools are referenced in plans
- `enforce-before-implement.sh`: Main wrapper that calls both enforcement hooks

### 2. Tracking Files
- `.claude/current_subagent_assigned`: Tracks which subagent is assigned
- `.claude/current_skills_activated`: Tracks currently activated skills
- `.skills/active_skills.json`: Machine-readable skill tracking
- `.claude/plan.txt`: Plan file that must contain MCP_CALL markers

### 3. Integration Point
- Modified `sp.implement.md` to include enforcement check as first step

## Enforcement Rules

### Subagent Requirement
- Execution will abort if no valid subagent is assigned
- Subagent must be specified in `.claude/current_subagent_assigned`
- Value must not be "none", "unassigned", or empty

### Skill Activation Requirement
- At least one skill must be activated
- Skills must be listed in `.claude/current_skills_activated`
- Machine-readable tracking in `.skills/active_skills.json`

### MCP Usage Requirement
- Plan must contain MCP_CALL markers
- Direct ORM/database calls are forbidden during implementation
- All backend operations must go through MCP tools

## Validation Process

1. **Pre-Implementation Check**: Validates subagent assignment and skill activation
2. **Pre-MCP Check**: Validates MCP tool usage in plans
3. **Artifact Validation**: Ensures all required tracking files exist
4. **Hard Failure**: Aborts execution if any check fails

## Integration with Implementation

The enforcement system is integrated into the `/sp.implement` command:

1. **Step 1**: Execute `.claude/hooks/enforce-before-implement.sh`
2. **Validation**: Run all compliance checks
3. **Abort or Continue**: Stop if checks fail, proceed if all pass
4. **Implementation**: Continue with normal implementation process

## Failure Conditions

The system will abort with exit code 1 if:
- No subagent assigned in `.claude/current_subagent_assigned`
- No skills activated in `.claude/current_skills_activated`
- No MCP_CALL markers in `.claude/plan.txt`
- Required tracking files are missing
- Any validation check fails

## Success Conditions

Implementation proceeds only when:
- ✅ Valid subagent is assigned
- ✅ At least one skill is activated
- ✅ MCP_CALL markers exist in plan
- ✅ All tracking artifacts are present
- ✅ All validation checks pass

## Benefits

- **Mandatory Compliance**: Cannot bypass requirements
- **Automatic Enforcement**: Runs without manual intervention
- **Fail-Safe Design**: Stops execution on any violation
- **Traceability**: All requirements are tracked and verifiable
- **Integration**: Built into the implementation workflow

This system ensures that Claude follows the required patterns of using subagents, skills, and MCP tools for all implementation work.