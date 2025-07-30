[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/simplemindedbot-crewai-test-badge.png)](https://mseep.ai/app/simplemindedbot-crewai-test)

# AI Agent Swarm Research System

> 🤖 Self-hosted, open-source swarm of AI agents for end-to-end research on arbitrary topics

A sophisticated multi-agent research system built with **CrewAI** orchestration, **LLMLingua** prompt compression, and dynamic **MCP (Model Context Protocol)** integration for cost-effective, extensible AI research workflows.

## 🚀 Overview

This project enables autonomous research teams of AI agents to collaborate on complex research tasks. The system automatically discovers sources, summarizes findings, validates information, and produces comprehensive research reports while minimizing token costs through intelligent prompt compression.

### Key Features

- **🎯 Multi-Agent Orchestration**: Specialized agents (Researcher, Summarizer, Validator) work in coordinated workflows
- **💰 Cost Optimization**: LLMLingua compression reduces token usage by 50%+ with minimal quality impact
- **🔧 Dynamic Tool Integration**: MCP protocol enables runtime addition of new tools and services
- **📊 Research Intelligence**: End-to-end research workflows with fact-checking and validation
- **🔄 Memory Persistence**: Agents maintain context and learn across research sessions
- **📈 Monitoring & Metrics**: Built-in token usage, latency, and accuracy tracking

## 🏗️ Architecture

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

## 🛠️ Tech Stack

- **Orchestration**: [CrewAI](https://crewai.com) - Multi-agent coordination and task management
- **Compression**: [LLMLingua](https://github.com/microsoft/LLMLingua) - Intelligent prompt compression
- **Tool Protocol**: [MCP](https://modelcontextprotocol.io) - Dynamic tool discovery and integration
- **Language**: Python 3.10+ with UV dependency management
- **Memory**: Vector embeddings for persistent agent memory
- **Monitoring**: Prometheus metrics and observability

## 🚦 Current Status

**Phase**: Foundation Setup ✅  
**Current Sprint**: Sprint 1 - Environment & Core Prototype  
**Next Milestone**: MVP with multi-agent flow (Sprint 2)

### Working Features
- ✅ Basic CrewAI research workflow
- ✅ Researcher and Analyst agent roles  
- ✅ Markdown report generation
- ✅ YAML-based agent/task configuration

### In Development (14-week roadmap)
- 🔄 **Sprint 1**: CI pipeline and memory persistence
- 📋 **Sprint 2**: Multi-agent flows with specialized roles
- 📋 **Sprint 3**: LLMLingua prompt compression integration
- 📋 **Sprint 4**: MCP dynamic tool loading
- 📋 **Sprint 5**: Runtime tool discovery and failover
- 📋 **Sprint 6**: Complete research workflow automation
- 📋 **Sprint 7**: Production deployment and monitoring

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ (3.14 max)
- OpenAI API key or compatible LLM API
- UV package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/simplemindedbot/crewai-test.git
cd crewai-test

# Install dependencies
crewai install
# or: pip install uv && uv sync

# Configure environment
cp .env.example .env
# Add your OPENAI_API_KEY to .env
```

### Basic Usage

```bash
# Run the research crew
crewai run

# Alternative entry points
crewai_test
run_crew

# Training and testing
train <iterations> <filename>
test <iterations> <eval_llm>
replay <task_id>
```

### Example Research Flow

The system currently researches "AI LLMs" by default and produces a detailed markdown report. You can customize the research topic by modifying the inputs in `src/crewai_test/main.py`.

## 📂 Project Structure

```
crewai_test/
├── src/crewai_test/
│   ├── config/
│   │   ├── agents.yaml      # Agent role definitions
│   │   └── tasks.yaml       # Task configurations
│   ├── crew.py              # Main crew orchestration
│   ├── main.py              # Entry points and CLI
│   └── tools/               # Custom tools and integrations
├── DEVPLAN.md               # 14-week development roadmap
├── CLAUDE.md                # Project documentation for AI assistants
└── README.md                # This file
```

## 🎯 Development Roadmap

Our [comprehensive development plan](DEVPLAN.md) spans 14 weeks across 7 focused sprints:

| Sprint | Focus Area | Timeline | Key Deliverables |
|--------|------------|----------|------------------|
| **1** | Foundation Setup | 2 weeks | CI/CD, Memory Persistence |
| **2** | Agent Architecture | 2 weeks | Multi-agent Workflows |
| **3** | Cost Optimization | 2 weeks | LLMLingua Integration |
| **4** | Tool Extensibility | 2 weeks | MCP Client Integration |
| **5** | Dynamic Discovery | 2 weeks | Runtime Tool Loading |
| **6** | Research Automation | 2 weeks | End-to-end Workflows |
| **7** | Production Ready | 2 weeks | Testing & Deployment |

## 🤝 Contributing

We welcome contributions! Please see our [GitHub Issues](https://github.com/simplemindedbot/crewai-test/issues) for current development priorities.

### Development Setup

```bash
# Clone and setup development environment
git clone https://github.com/simplemindedbot/crewai-test.git
cd crewai-test
crewai install

# Run tests (when available)
pytest

# Code formatting
black src/
isort src/
```

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🔗 Related Projects

- [CrewAI](https://github.com/joaomdmoura/crewai) - Multi-agent orchestration framework
- [LLMLingua](https://github.com/microsoft/LLMLingua) - Prompt compression library
- [Model Context Protocol](https://modelcontextprotocol.io) - Universal tool integration standard

## 📧 Contact & Support

- **Issues**: [GitHub Issues](https://github.com/simplemindedbot/crewai-test/issues)
- **Documentation**: [Project Wiki](https://github.com/simplemindedbot/crewai-test/wiki)
- **CrewAI Community**: [Discord](https://discord.com/invite/X4JWnZnxPb)

---

**Built with ❤️ for the AI research community**