#!/bin/bash
# Pre-Implementation Enforcement Hook
# Ensures that subagents and skills are properly assigned before /sp.implement execution
# Aborts /sp.implement if compliance checks fail

set -euo pipefail  # Exit on error, undefined vars, and pipe failures

echo "🔍 Running pre-implementation enforcement check..."

# Check if subagent is assigned
SUBAGENT_FILE=".claude/current_subagent_assigned"
if [[ ! -f "$SUBAGENT_FILE" ]] || [[ ! -s "$SUBAGENT_FILE" ]]; then
    echo "❌ ERROR: No subagent assigned for current task"
    echo "❌ File $SUBAGENT_FILE does not exist or is empty"
    echo "❌ Please assign a subagent before running /sp.implement"
    exit 1
else
    ASSIGNED_SUBAGENT=$(cat "$SUBAGENT_FILE" | tr -d '\n\r ')
    if [[ -z "$ASSIGNED_SUBAGENT" ]] || [[ "$ASSIGNED_SUBAGENT" == "none" ]] || [[ "$ASSIGNED_SUBAGENT" == "unassigned" ]]; then
        echo "❌ ERROR: Invalid or unassigned subagent in $SUBAGENT_FILE"
        echo "❌ Current value: '$ASSIGNED_SUBAGENT'"
        exit 1
    fi
    echo "✅ Subagent assigned: $ASSIGNED_SUBAGENT"
fi

# Check if skills are activated
SKILLS_ACTIVATED_FILE=".claude/current_skills_activated"
if [[ ! -f "$SKILLS_ACTIVATED_FILE" ]] || [[ ! -s "$SKILLS_ACTIVATED_FILE" ]]; then
    echo "❌ ERROR: No skills activated for current task"
    echo "❌ File $SKILLS_ACTIVATED_FILE does not exist or is empty"
    echo "❌ Please activate at least one relevant skill before running /sp.implement"
    exit 1
else
    ACTIVE_SKILLS_COUNT=$(wc -l < "$SKILLS_ACTIVATED_FILE" | tr -d ' ')
    if [[ $ACTIVE_SKILLS_COUNT -eq 0 ]]; then
        echo "❌ ERROR: No active skills found in $SKILLS_ACTIVATED_FILE"
        exit 1
    fi
    echo "✅ Active skills file exists with $ACTIVE_SKILLS_COUNT entries"
fi

# Check machine-readable skill artifacts
ACTIVE_SKILLS_JSON=".skills/active_skills.json"
if [[ ! -f "$ACTIVE_SKILLS_JSON" ]]; then
    echo "❌ ERROR: Machine-readable skill artifacts file missing"
    echo "❌ File $ACTIVE_SKILLS_JSON does not exist"
    echo "❌ Please ensure skills are properly tracked in JSON format"
    exit 1
else
    if ! command -v jq >/dev/null 2>&1; then
        # If jq is not available, at least check if it's a valid JSON file
        if ! python3 -m json.tool < "$ACTIVE_SKILLS_JSON" >/dev/null 2>&1; then
            echo "❌ ERROR: $ACTIVE_SKILLS_JSON is not valid JSON"
            exit 1
        fi
    else
        # Validate JSON with jq
        if ! jq empty "$ACTIVE_SKILLS_JSON" 2>/dev/null; then
            echo "❌ ERROR: $ACTIVE_SKILLS_JSON is not valid JSON"
            exit 1
        fi
    fi
    echo "✅ Machine-readable skill artifacts validated"
fi

# Check plan file for MCP_CALL markers
PLAN_FILE=".claude/plan.txt"
if [[ ! -f "$PLAN_FILE" ]]; then
    echo "❌ ERROR: Plan file missing"
    echo "❌ File $PLAN_FILE does not exist"
    echo "❌ Please ensure a plan exists before running /sp.implement"
    exit 1
else
    # Check if MCP_CALL markers exist in the plan
    if ! grep -q "MCP_CALL" "$PLAN_FILE"; then
        echo "❌ ERROR: No MCP_CALL markers found in $PLAN_FILE"
        echo "❌ Plan must reference MCP tools for backend operations"
        echo "❌ Add MCP_CALL markers to indicate MCP tool usage"
        exit 1
    fi
    MCP_CALL_COUNT=$(grep -c "MCP_CALL" "$PLAN_FILE")
    echo "✅ Plan file contains $MCP_CALL_COUNT MCP_CALL markers"
fi

# Additional validation: Check that plan doesn't contain direct ORM/database calls
if grep -i -E "(sqlmodel|sqlalchemy|database\.execute|session\.execute|orm|raw sql|direct database)" "$PLAN_FILE" | grep -v "MCP_CALL"; then
    echo "⚠️  WARNING: Plan may contain direct database references without MCP_CALL markers"
    echo "⚠️  Ensure all database operations go through MCP tools, not direct ORM calls"
    # We'll allow this as a warning for now, but it should be addressed
fi

echo "✅ All pre-implementation enforcement checks passed!"
echo "🚀 Subagent: $ASSIGNED_SUBAGENT"
echo "🎯 Active skills: $ACTIVE_SKILLS_COUNT"
echo "🔗 MCP integration: $MCP_CALL_COUNT references"
echo "✨ Ready to proceed with /sp.implement"

exit 0