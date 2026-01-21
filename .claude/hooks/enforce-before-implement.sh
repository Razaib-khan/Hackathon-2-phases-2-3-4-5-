#!/bin/bash
# Wrapper script to enforce compliance before any implementation begins
# This script should be called as part of the implementation process

set -euo pipefail

echo "🔒 ENFORCEMENT CHECK: Starting compliance validation..."
echo " "

# Check if we're in an implementation context by checking for tasks.md
if [[ ! -f "specs/*/tasks.md" ]] && [[ ! -f "./tasks.md" ]]; then
    echo "⚠️  WARNING: No tasks.md found in expected locations"
    echo "⚠️  This might not be an implementation context, but running enforcement anyway"
fi

echo "🔍 Running pre-implementation enforcement checks..."
echo " "

# Call the main enforcement hook
if [[ -f ".claude/hooks/pre-implement-enforce-subagents.sh" ]]; then
    echo "[ENFORCEMENT] Calling subagent enforcement hook..."
    .claude/hooks/pre-implement-enforce-subagents.sh
    RESULT=$?
    if [[ $RESULT -ne 0 ]]; then
        echo "❌ SUBAGENT ENFORCEMENT FAILED - Implementation blocked"
        echo "❌ Please ensure:"
        echo "❌ 1. A subagent is assigned in .claude/current_subagent_assigned"
        echo "❌ 2. Skills are activated in .claude/current_skills_activated"
        echo "❌ 3. MCP_CALL markers exist in .claude/plan.txt"
        echo "❌ 4. Machine-readable skills exist in .skills/active_skills.json"
        exit 1
    fi
else
    echo "❌ ERROR: Pre-implementation enforcement hook not found"
    exit 1
fi

echo " "
echo "🔍 Running pre-MCP enforcement checks..."
echo " "

# Call the MCP enforcement hook
if [[ -f ".claude/hooks/pre-mcp-enforce.sh" ]]; then
    echo "[ENFORCEMENT] Calling MCP enforcement hook..."
    .claude/hooks/pre-mcp-enforce.sh
    RESULT=$?
    if [[ $RESULT -ne 0 ]]; then
        echo "❌ MCP ENFORCEMENT FAILED - Implementation blocked"
        echo "❌ Please ensure MCP_CALL markers exist in your plan"
        exit 1
    fi
else
    echo "❌ ERROR: Pre-MCP enforcement hook not found"
    exit 1
fi

echo " "
echo "✅ ALL ENFORCEMENT CHECKS PASSED!"
echo "🚀 Implementation can proceed safely"
echo " "
echo "📋 Enforcement Summary:"
echo "   • Subagent assigned and validated"
echo "   • Skills activated and tracked"
echo "   • MCP tools referenced in plan"
echo "   • All required artifacts present"
echo " "

exit 0