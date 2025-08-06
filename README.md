# AI Agent Swarm Research System

[![Verified on MSeeP](https://mseep.ai/badge.svg)](https://mseep.ai/app/2cc20da7-cfe8-4fa9-abbb-10502ecd36a6)

> 🤖 Self-hosted, open-source swarm of AI agents for end-to-end research on arbitrary topics

A sophisticated multi-agent research system built with **CrewAI** orchestration, **LLMLingua** prompt compression, and dynamic **MCP (Model Context Protocol)** integration for cost-effective, extensible AI research workflows.

## 🚀 Overview

This project enables autonomous research teams of AI agents to collaborate on complex research tasks. The system automatically discovers sources, summarizes findings, validates information, and produces comprehensive research reports while minimizing token costs through intelligent prompt compression.

### Key Features

- **🎯 Multi-Agent Orchestration**: Specialized agents (Researcher, Summarizer, Validator, Coordinator) work in coordinated workflows
- **🧠 Enhanced Memory System**: Vector embeddings with semantic search for cross-agent knowledge sharing
- **💰 Cost Optimization**: LLMLingua compression reduces token usage by 50%+ with minimal quality impact
- **🔧 Dynamic Tool Integration**: MCP protocol enables runtime addition of new tools and services
- **📊 Research Intelligence**: End-to-end research workflows with fact-checking and validation
- **🔄 Memory Persistence**: Agents maintain context and learn across research sessions with FAISS-powered semantic search
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
- **Memory**: Vector embeddings with FAISS and sentence-transformers for semantic search
- **Monitoring**: Prometheus metrics and observability

## 🚦 Current Status

**Phase**: Multi-Agent Architecture ✅  
**Current Sprint**: Sprint 2 Complete - Multi-Agent Research Workflow  
**Next Milestone**: LLMLingua prompt compression integration (Sprint 3)

### Working Features
- ✅ **Multi-Agent Research System**: ResearcherAgent, SummarizerAgent, ValidatorAgent, CoordinatorAgent
- ✅ **Sequential Workflow**: Researcher → Summarizer → Validator → Coordinator with task dependencies
- ✅ **Enhanced Memory Store**: Vector embeddings with FAISS for semantic search and cross-agent memory sharing
- ✅ **Cross-Agent Recall**: Agents can access facts and context from other agents across task executions
- ✅ **Comprehensive Testing**: Automated tests for memory persistence, cross-agent recall, and semantic search
- ✅ **YAML Configuration**: Flexible agent and task configuration system
- ✅ **CI/CD Pipeline**: Automated testing, linting, and quality assurance
- ✅ **Memory Analytics**: Detailed analytics for embeddings, agent distribution, and memory usage

### Development Progress (14-week roadmap)
- ✅ **Sprint 1**: CI pipeline and memory persistence
- ✅ **Sprint 2**: Multi-agent flows with enhanced memory system
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

### Sprint 2: Multi-Agent Research Demo

Test the complete multi-agent research workflow:

```bash
# Set up environment
export $(cat .env | xargs)
cd crewai_test

# Run multi-agent research crew
PYTHONPATH=src python src/crewai_test/research_main.py "artificial intelligence trends"

# Test enhanced memory system
PYTHONPATH=src python src/crewai_test/test_enhanced_memory.py

# Test cross-agent fact recall
PYTHONPATH=src python src/crewai_test/test_cross_agent_recall.py
```

The multi-agent system demonstrates:
- ✅ Four specialized agents working in sequence
- ✅ Enhanced memory with vector embeddings and semantic search
- ✅ Cross-agent memory sharing and fact recall
- ✅ Comprehensive research workflow from discovery to final report

### Sprint 1: Echo Agent Demo

For basic functionality testing:

```bash
# Test basic echo functionality
export $(cat .env | xargs)
cd crewai_test
PYTHONPATH=src python src/crewai_test/echo_main.py "Hello, World!"

# Test memory persistence across sessions
PYTHONPATH=src python src/crewai_test/test_memory_persistence.py
```

## 📂 Project Structure

```
crewai_test/
├── src/crewai_test/
│   ├── config/
│   │   ├── agents.yaml          # Basic agent role definitions
│   │   ├── agents_research.yaml # Multi-agent research configuration
│   │   ├── agents_echo.yaml     # Echo agent for testing
│   │   ├── tasks.yaml           # Basic task configurations
│   │   ├── tasks_research.yaml  # Multi-agent research tasks
│   │   └── tasks_echo.yaml      # Echo tasks for testing
│   ├── crew.py                  # Basic crew orchestration
│   ├── research_crew.py         # Multi-agent research crew
│   ├── echo_crew.py            # Echo agent for testing
│   ├── memory_store.py         # Basic memory persistence
│   ├── enhanced_memory_store.py # Vector embeddings memory system
│   ├── main.py                 # Entry points and CLI
│   ├── research_main.py        # Multi-agent research entry point
│   ├── test_enhanced_memory.py # Enhanced memory system tests
│   ├── test_cross_agent_recall.py # Cross-agent memory tests
│   └── tools/                  # Custom tools and integrations
├── DEVPLAN.md                  # 14-week development roadmap
├── SPRINT1.md                  # Sprint 1 detailed breakdown
├── SPRINT2.md                  # Sprint 2 detailed breakdown
├── MEMORY_PERSISTENCE.md       # Memory system documentation
├── CLAUDE.md                   # Project documentation for AI assistants
└── README.md                   # This file
```

## 🎯 Development Roadmap

Our [comprehensive development plan](DEVPLAN.md) spans 14 weeks across 7 focused sprints:

| Sprint | Focus Area | Timeline | Status | Key Deliverables |
|--------|------------|----------|--------|------------------|
| **1** | Foundation Setup | 2 weeks | ✅ Complete | CI/CD, Memory Persistence |
| **2** | Agent Architecture | 2 weeks | ✅ Complete | Multi-agent Workflows, Enhanced Memory |
| **3** | Cost Optimization | 2 weeks | 📋 Planned | LLMLingua Integration |
| **4** | Tool Extensibility | 2 weeks | 📋 Planned | MCP Client Integration |
| **5** | Dynamic Discovery | 2 weeks | 📋 Planned | Runtime Tool Loading |
| **6** | Research Automation | 2 weeks | 📋 Planned | End-to-end Workflows |
| **7** | Production Ready | 2 weeks | 📋 Planned | Testing & Deployment |

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

[![MseeP.ai Security Assessment Badge](https://mseep.net/pr/simplemindedbot-crewai-test-badge.png)](https://mseep.ai/app/simplemindedbot-crewai-test)

**Built with ❤️ for the AI research community**
