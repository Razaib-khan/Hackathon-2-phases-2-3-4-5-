---
name: openai-agents-python-openrouter
description: Authoritative guidance for building production-grade Python agents using the OpenAI Agents SDK, including tools, handoffs, structured outputs, guardrails, and integration with OpenRouter for multi-provider LLM execution.
---

# OpenAI Agents SDK (Python) + OpenRouter

## Purpose
This skill defines best practices, architecture, and execution patterns for using the **OpenAI Agents SDK (Python)** to orchestrate AI agents while optionally delegating model inference to **OpenRouter** for access to multiple LLM providers.

Use this skill to build reliable, maintainable, and scalable agent systems.

## When to Use
Invoke this skill when the task involves:
- OpenAI Agents SDK (Python)
- Agent, Runner, tools, or handoffs
- Multi-agent workflows or triage agents
- Structured outputs with validation
- Guardrails and failure handling
- Calling OpenRouter models from Python
- Cost, latency, or model-routing concerns

## Core Architecture

### Agent
An Agent encapsulates:
- Instructions (system behavior)
- Optional tools
- Optional handoffs to other agents
- Optional output schema

Agents do not execute directly.

### Runner
The Runner:
- Executes agents
- Handles tool calls
- Manages handoffs
- Enforces guardrails
- Collects traces

All execution flows through `Runner.run(...)`.

### Tools
Tools are deterministic Python callables exposed to agents.
They may:
- Perform computation
- Call APIs
- Access external services
- Act as integration boundaries

Business logic belongs in tools, not prompts.

### Handoffs
Handoffs allow an agent to delegate tasks to other agents based on intent or specialization.
This enables:
- Triage patterns
- Specialist agents
- Modular reasoning pipelines

### Structured Outputs
Agents may return validated structured data using:
- Pydantic models
- TypedDict
- Dataclasses

Structured outputs are required for automation and safety.

### Guardrails
Guardrails validate:
- Inputs before execution
- Outputs before returning results

Invalid outputs must be rejected or retried.

## OpenRouter Integration

### Integration Reality
OpenRouter is not natively supported by the OpenAI Agents SDK.
It must be integrated manually as an external inference layer.

Implications:
- OpenAI-hosted tools do not apply to OpenRouter calls
- All OpenRouter responses must be validated
- Error handling is mandatory

### Recommended Pattern
- Use OpenAI Agents SDK for orchestration
- Use OpenRouter strictly for model inference
- Wrap OpenRouter calls inside a dedicated tool
- Normalize and validate all responses

### Execution Flow
1. Agent determines external inference is required
2. Agent calls an OpenRouter tool
3. Tool sends request to OpenRouter `/chat/completions`
4. Tool returns normalized output
5. Agent validates output via schema or guardrail

## Best Practices

### Model Strategy
- Prefer OpenAI models for tool-heavy workflows
- Use OpenRouter for:
  - Cost optimization
  - Provider diversity
  - Specialized reasoning or writing
- Keep temperatures low for deterministic tasks

### Fallbacks
- Attempt cheaper models first
- Escalate on failure
- Track latency and token usage

### Prompt Discipline
- Prompts express intent
- Tools perform actions
- Never embed logic in prompts

### Observability
- Inspect Runner traces
- Treat unexpected tool calls as defects
- Validate all external model outputs

## Supported Prompt Examples

Design a Python agent using OpenAI Agents SDK that routes summarization
tasks to OpenRouter and validates output with Pydantic.

Copy code
Explain how to build a triage agent that delegates math questions to one
agent and reasoning-heavy tasks to an OpenRouter-backed agent.

Copy code
Show the correct architecture for integrating OpenRouter into an OpenAI
Agents SDK workflow without bypassing guardrails.

markdown
Copy code

## Constraints
- Do not assume OpenRouter supports OpenAI hosted tools
- Do not bypass validation for external model outputs
- Do not mix orchestration logic with inference logic

## Output Requirements
Responses using this skill must:
- Be Python-focused
- Use OpenAI Agents SDK terminology correctly
- Separate orchestration from inference
- Emphasize correctness, validation, and maintainability