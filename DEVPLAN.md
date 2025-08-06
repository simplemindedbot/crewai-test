# Development Plan for CrewAI Swarm Research System

This document outlines the development plan for a self-hosted, open-source swarm of AI agents designed to perform end-to-end research on arbitrary topics. The system will utilize CrewAI for orchestration, LLMLingua for prompt compression, and support dynamic Model Context Protocol (MCP) integration.

# Objectives

* Enable a self‑hosted, open‑source swarm of AI agents to perform end‑to‑end research on arbitrary topics.
* Use **CrewAI** as the orchestration framework for agent coordination, task delegation and shared memory.
* Incorporate **LLMLingua** for prompt compression to maximize token efficiency and reduce LLM costs.
* Support **dynamic MCP** (Model Context Protocol) integration so new tool servers can be added at runtime, regardless of runtime (Python/UV, Node, remote HTTP).

---

## 1. Architecture Overview

```text
┌─────────────────────────────────────────────┐
│                 Coordinator                │
│             (CrewAI Orchestrator)          │
│  • Manages Shared State & Memory           │
│  • Dispatches Researcher / Summarizer      │
│    / Validator Agents                      │
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

* **Coordinator**: CrewAI process that defines agent “Crews” and “Flows.”
* **Agent Middleware**:

  * **LLMLingua** compressor wraps every outbound prompt.
  * **MCP Client** discovers & invokes tool servers via JSON‑RPC.
* **Execution Targets**: LLM endpoints for inference; MCP servers for tools; any other services.

---

## 2. Component Breakdown

| Component              | Responsibility                                                                       |
| ---------------------- | ------------------------------------------------------------------------------------ |
| **CrewAI Core**        | Multi‐agent orchestration, task routing, memory store                                |
| **Agent Roles**        | — Researcher: gathers sources<br>— Summarizer: condenses<br>— Validator: fact‑checks |
| **LLMLingua Service**  | Compress prompts before LLM call                                                     |
| **MCP Integration**    | Dynamically load tool definitions, call tools                                        |
| **Tool Registry**      | YAML/JSON manifest listing MCP endpoints                                             |
| **Deployment Scripts** | Docker/Helm for orchestrator and servers                                             |

---

## 3. Development Roadmap

### Sprint 1: Environment & Core Prototype (2 weeks)

* **Setup**

  * Initialize Git repo.
  * Python venv / Poetry; pin CrewAI stable release.
  * CI pipeline: lint, type‑check, unit tests.
* **CrewAI “Hello World”**

  * Define a minimal Crew with one agent that echoes inputs.
  * Validate CrewAI installation and memory persistence.

### Sprint 2: Agent Role Definitions & Flows (2 weeks)

* **Define Agent Classes**

  * `ResearcherAgent`, `SummarizerAgent`, `ValidatorAgent`.
* **Implement Flows**

  * **Flow A**: Researcher → Summarizer → Validator → Coordinator.
  * Add CrewAI Tasks for each sub‑action.
* **Shared State**

  * Configure long‑term memory store (embeddings).
  * Verify that agents recall facts across tasks.

### Sprint 3: LLMLingua Integration (2 weeks)

* **Install LLMLingua**

  ```bash
  pip install llmlingua
  ```

* **Middleware**

  ```python
  from crewai.middleware import TransformMiddleware
  from llmlingua import PromptCompressor

  compressor = PromptCompressor(model_name="llmlingua-2")

  def compress(text: str) -> str:
      return compressor.compress(text)

  crew = Crew(
      ...,
      middlewares=[TransformMiddleware(on_send=compress)]
  )
  ```

* **Validation**

  * Benchmark token reduction on sample prompts (> 50% reduction).
  * Ensure LLM responses remain within 5% of uncompressed quality.

### Sprint 4: MCP Client Integration (2 weeks)

* **Select SDK**

  ```bash
  pip install modelcontextprotocol dolphin-mcp
  ```

* **Config Loader**

  ```yaml
  # config/mcp_servers.yaml
  mcp_servers:
    - name: github
      type: http
      url: https://mcp.github.com
    - name: code_runner
      type: stdio
      command: uvx mcp-code-runner
  ```

* **Client Adapter**

  * On agent startup, load YAML and `discover_servers()`.
  * Wrap MCP tool calls as CrewAI tools:

    ```python
    from crewai.tools import register_tool
    from mcp.client import MCPClient

    client = MCPClient.from_config("config/mcp_servers.yaml")
    for tool in client.list_tools():
        register_tool(tool.name, lambda args: client.call_tool(tool.name, args))
    ```

* **E2E Test**

  * Connect to a local “weather” MCP server; verify `get_forecast` via an agent flow.

### Sprint 5: Dynamic Tool Registry & Failover (2 weeks)

* **Dynamic Discovery**

  * Implement Watcher to reload `mcp_servers.yaml` on change.
  * Agents re-scan available tools without restart.
* **Failover Logic**

  * If HTTP server unreachable, fallback to STDIO or alternate endpoint.
  * Log tool latencies & errors for monitoring.
* **Example**

  ```yaml
  mcp_servers:
    - name: ai_math
      type: stdio
      command: uvx mcp-math
      fallback: http://backup.math-server.local
  ```

### Sprint 6: End‑to‑End Swarm Research Workflow (2 weeks)

* **Scenario**: “Impact of X on Y” research
* **Steps**

  1. ResearcherAgent fetches web sources via MCP web-scraper tools.
  2. SummarizerAgent compresses & summarizes findings.
  3. ValidatorAgent runs fact‑checks via MCP knowledge‑base tools.
  4. Coordinator aggregates, writes final report.
* **Metrics**

  * Total tokens (before/after compression).
  * Latency per agent step.
  * Accuracy of summaries vs. baseline.

### Sprint 7: Testing, Monitoring & Documentation (2 weeks)

* **Testing**

  * Unit tests for middleware, MCP adapter, agent logic.
  * Integration tests for full flow with mock LLM & mock MCP servers.
* **Monitoring**

  * Instrument token usage, agent success rates.
  * Expose Prometheus metrics via a small HTTP server.
* **Documentation**

  * Architecture diagrams (Mermaid).
  * README with quickstart and YAML examples.
  * Contribution guide.
* **Deployment**

  * Docker Compose for orchestrator + example MCP servers.
  * Helm chart templates for Kubernetes deployment.

---

## 4. Milestones & Success Criteria

| Milestone                             | Criteria                                                                                                                  |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| **MVP Prototype** (end Sprint 2)      | Single‑agent echo Crew; basic CrewAI flow runs; memory persists.                                                          |
| **Compression Live** (end Sprint 3)   | LLMLingua reduces tokens by ≥ 50%; no regression in response quality (> 95% accuracy).                                    |
| **MCP Tooling** (end Sprint 4)        | Agents discover ≥ 2 MCP servers; invoke functions successfully (e.g. weather, code\_runner).                              |
| **Dynamic Extensibility** (Sprint 5)  | Add/modify `mcp_servers.yaml` at runtime; agents pick up new tools without restart; failover tested.                      |
| **Full Research Workflow** (Sprint 6) | Agents complete multistep research task end‑to‑end; reports generated; token & latency metrics captured.                  |
| **Production Readiness** (Sprint 7)   | 80%+ code coverage; CI/CD pipeline in place; docs published; containerized deployment tested; monitoring dashboards live. |

---

## 5. Risks & Mitigations

* **Integration Complexity**

  * *Mitigation*: Feature‑flag LLMLingua and MCP early; isolate in middleware for easy rollback.
* **Compression Quality**

  * *Mitigation*: Establish quality benchmarks; allow bypass of compressor per‑flow if issues arise.
* **MCP Spec Changes**

  * *Mitigation*: Pin SDK versions; include automated compatibility tests in CI for client–server handshake.
* **Performance Overhead**

  * *Mitigation*: Profile middleware; cache compressed prompts; consider async compression.

---

## 6. Next Steps

1. **Kick‑off Planning**: Assign roles (Backend, DevOps, QA) to Claude Code.
2. **Backlog Grooming**: Break sprints into JIRA tickets or GitHub issues.
3. **Infrastructure Setup**: Provision CI/CD, container registry, testbed servers.
4. **Sprint 1 Start**: Clone repos, establish environments, commit initial CrewAI prototype.

This plan provides a clear, phased approach to deliver a token‑efficient, extensible swarm research system leveraging CrewAI, LLMLingua, and MCP.
