# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Vision

**Objective**: Build a self-hosted, open-source swarm of AI agents for end-to-end research on arbitrary topics using CrewAI orchestration, LLMLingua prompt compression, and dynamic MCP (Model Context Protocol) integration.

## Current State

CrewAI test project with basic research workflow. Uses Python >=3.10 <3.14, UV for dependency management, and includes LLMLingua. Currently generates `report.md` about AI LLMs research.

## Target Architecture

```
┌─────────────────────────────────────────────┐
│                 Coordinator                │
│             (CrewAI Orchestrator)          │
│  • Manages Shared State & Memory           │
│  • Dispatches Research/Summarizer/         │
│    Validator Agents                        │
└─────────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────┐
│             Agent Middleware               │
│  • LLMLingua PromptCompressor              │
│  • MCP Client Adapter                      │
└─────────────────────────────────────────────┘
                │
                ▼
┌───────────┬───────────────┬────────────────┐
│  LLM API  │  MCP Server   │  External APIs │
│ (GPT, etc)│ (any protocol)│ (web, DB, etc) │
└───────────┴───────────────┴────────────────┘
```

## Development Roadmap (14 Weeks Total)

### Sprint 1: Environment & Core Prototype (2 weeks)
- Initialize Git repo with CI pipeline (lint, type-check, unit tests)
- CrewAI "Hello World" with minimal crew and memory persistence
- **Milestone**: Single-agent echo Crew with persistent memory

### Sprint 2: Agent Role Definitions & Flows (2 weeks)
- Define `ResearcherAgent`, `SummarizerAgent`, `ValidatorAgent` classes
- Implement Flow: Researcher → Summarizer → Validator → Coordinator
- Configure long-term memory store with embeddings
- **Milestone**: MVP Prototype with multi-agent flow

### Sprint 3: LLMLingua Integration (2 weeks)
- Install and integrate LLMLingua prompt compression middleware
- Wrap outbound prompts with compressor in CrewAI TransformMiddleware
- Benchmark ≥50% token reduction with <5% quality degradation
- **Milestone**: Compression Live with validated performance

### Sprint 4: MCP Client Integration (2 weeks)
- Install MCP SDK and create config loader for `mcp_servers.yaml`
- Build client adapter to wrap MCP tools as CrewAI tools
- E2E test with local MCP server (e.g., weather service)
- **Milestone**: MCP Tooling with ≥2 servers connected

### Sprint 5: Dynamic Tool Registry & Failover (2 weeks)
- Implement file watcher for runtime `mcp_servers.yaml` reload
- Add failover logic (HTTP → STDIO → alternate endpoint)
- Enable agents to discover new tools without restart
- **Milestone**: Dynamic Extensibility with runtime tool discovery

### Sprint 6: End-to-End Swarm Research Workflow (2 weeks)
- Implement full research scenario: "Impact of X on Y"
- ResearcherAgent → web scraping via MCP tools
- SummarizerAgent → content compression and summarization
- ValidatorAgent → fact-checking via knowledge-base tools
- Coordinator → final report aggregation
- **Milestone**: Full Research Workflow with metrics

### Sprint 7: Testing, Monitoring & Documentation (2 weeks)
- 80%+ code coverage with unit and integration tests
- Prometheus metrics for token usage and agent success rates
- Architecture documentation with Mermaid diagrams
- Docker Compose and Helm chart deployment
- **Milestone**: Production Readiness

## Component Responsibilities

| Component              | Responsibility                                                                       |
| ---------------------- | ------------------------------------------------------------------------------------ |
| **CrewAI Core**        | Multi-agent orchestration, task routing, memory store                                |
| **Agent Roles**        | Researcher: sources, Summarizer: condenses, Validator: fact-checks |
| **LLMLingua Service**  | Compress prompts before LLM call                                                     |
| **MCP Integration**    | Dynamically load tool definitions, call tools                                        |
| **Tool Registry**      | YAML/JSON manifest listing MCP endpoints                                             |
| **Deployment Scripts** | Docker/Helm for orchestrator and servers                                             |

## Current Development Commands

```bash
# Install dependencies
crewai install
# or: pip install uv && uv sync

# Run the crew (main command)
crewai run

# Alternative entry points
crewai_test
run_crew

# Training and testing
train <iterations> <filename>
test <iterations> <eval_llm>
replay <task_id>
```

## Current Architecture

**Core Structure:**
- `src/crewai_test/crew.py`: Main crew definition with @CrewBase decorator
- `src/crewai_test/main.py`: Entry points (run, train, replay, test)
- `config/agents.yaml`: Agent definitions (researcher, reporting_analyst)
- `config/tasks.yaml`: Task definitions (research_task, reporting_task)

**Workflow:** Sequential process where researcher agent conducts research, then reporting_analyst creates detailed markdown report.

**Configuration:** Agents and tasks use YAML configs with templating for topic and current_year variables.

**Environment:** Requires OPENAI_API_KEY in .env file.

## Risk Mitigations

- **Integration Complexity**: Feature-flag LLMLingua and MCP early; isolate in middleware
- **Compression Quality**: Establish quality benchmarks; allow bypass per-flow
- **MCP Spec Changes**: Pin SDK versions; automated compatibility tests in CI
- **Performance Overhead**: Profile middleware; cache compressed prompts; async compression