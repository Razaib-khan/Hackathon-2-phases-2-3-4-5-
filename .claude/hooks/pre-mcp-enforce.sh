#!/bin/bash
# Pre-MCP Enforcement Hook
# Ensures MCP tools are properly referenced in plans and implementations
# Validates that MCP usage is documented and tracked

set -euo pipefail  # Exit on error, undefined vars, and pipe failures

echo "🔍 Running pre-MCP enforcement check..."

# Check plan file exists
PLAN_FILE=".claude/plan.txt"
if [[ ! -f "$PLAN_FILE" ]]; then
    echo "❌ ERROR: Plan file missing"
    echo "❌ File $PLAN_FILE does not exist"
    echo "❌ MCP usage must be planned and documented"
    exit 1
fi

# Check for MCP_CALL markers
if ! grep -q "MCP_CALL" "$PLAN_FILE"; then
    echo "❌ ERROR: No MCP_CALL markers found in $PLAN_FILE"
    echo "❌ Plan must explicitly reference MCP tools for compliance"
    exit 1
fi

# Count MCP_CALL references
MCP_CALL_COUNT=$(grep -c "MCP_CALL" "$PLAN_FILE")
echo "✅ Found $MCP_CALL_COUNT MCP_CALL references in plan"

# Validate MCP_CALL format (should be followed by tool name)
MCP_TOOLS_REFERENCED=$(grep -o "MCP_CALL[^[:space:]]*" "$PLAN_FILE" | sort -u | wc -l)
if [[ $MCP_TOOLS_REFERENCED -eq 0 ]]; then
    echo "❌ ERROR: MCP_CALL markers found but no tool names referenced"
    echo "❌ Format should be 'MCP_CALL tool_name' or 'MCP_CALL: tool_name'"
    exit 1
fi

echo "✅ MCP_CALL markers properly formatted"

# Check if plan mentions direct database operations that should use MCP
if grep -i -E "(direct database|raw sql|sqlmodel\.select|sqlmodel\.insert|sqlmodel\.update|sqlmodel\.delete|session\.exec|session\.add|session\.commit)" "$PLAN_FILE"; then
    echo "❌ ERROR: Plan contains direct database operations that should use MCP tools"
    echo "❌ Replace direct ORM/SQL calls with MCP tool invocations"
    echo "❌ Examples: Use mcp__Neon__run_sql instead of direct SQLModel operations"
    exit 1
fi

# Check if current implementation stage requires MCP
IMPLEMENTATION_STAGE_FILE=".claude/current_stage"
if [[ -f "$IMPLEMENTATION_STAGE_FILE" ]]; then
    CURRENT_STAGE=$(cat "$IMPLEMENTATION_STAGE_FILE" | tr -d '\n\r ')
    if [[ "$CURRENT_STAGE" == "backend" ]] || [[ "$CURRENT_STAGE" == "database" ]] || [[ "$CURRENT_STAGE" == "api" ]]; then
        # These stages should definitely use MCP tools
        if [[ $MCP_CALL_COUNT -lt 1 ]]; then
            echo "❌ ERROR: Backend/database stage requires MCP tools but no MCP_CALL found"
            exit 1
        fi
        echo "✅ MCP usage appropriate for stage: $CURRENT_STAGE"
    fi
fi

# Verify that MCP tools are actually available
if command -v mcp >/dev/null 2>&1; then
    echo "✅ MCP tools are available in environment"
else
    # Even if mcp command isn't available, we can still validate the plan
    echo "⚠️  MCP command not found in environment (may be available during execution)"
fi

echo "✅ All pre-MCP enforcement checks passed!"
echo "🔗 MCP_CALL references: $MCP_CALL_COUNT"
echo "🔧 MCP tools: $MCP_TOOLS_REFERENCED unique references"

exit 0