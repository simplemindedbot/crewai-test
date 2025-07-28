# Memory Persistence Documentation

## Overview

The CrewAI Test project implements a dual-layer memory persistence system to ensure agents maintain context across runs and sessions. This system combines CrewAI's built-in memory capabilities with a custom file-based memory store.

## Architecture

### 1. CrewAI Built-in Memory
- **Long Term Memory**: Stores conversation history and insights
- **Short Term Memory**: Maintains working context during task execution  
- **Entity Memory**: Tracks important entities and their relationships

### 2. Custom File-Based Memory Store
- **SimpleMemoryStore**: JSON-based persistent storage
- **Cross-session persistence**: Survives application restarts
- **Interaction history**: Complete record of agent conversations
- **Fact storage**: Key information extraction and retention

## Memory Components

### SimpleMemoryStore Class

Located in `src/crewai_test/memory_store.py`, this class provides:

```python
class SimpleMemoryStore:
    def __init__(self, storage_path: str = "memory_store.json")
    def store_interaction(self, agent_name: str, input_message: str, output_message: str)
    def store_fact(self, agent_name: str, fact: str)
    def get_agent_history(self, agent_name: str) -> List[Dict[str, Any]]
    def get_recent_interactions(self, agent_name: str, limit: int = 5)
    def clear_agent_memory(self, agent_name: str)
```

### Features

1. **Automatic Persistence**: All interactions are automatically saved to disk
2. **Timestamped Entries**: Every interaction and fact includes ISO timestamps
3. **Agent-Specific Storage**: Separate memory spaces for different agents
4. **Context Injection**: Previous interactions are injected into new prompts
5. **Fact Extraction**: Important information is stored as retrievable facts

## Usage Examples

### Basic Memory Operations

```python
from crewai_test.memory_store import SimpleMemoryStore

# Initialize memory store
memory = SimpleMemoryStore("my_agent_memory.json")

# Store an interaction
memory.store_interaction("echo_agent", "Hello", "Hello")

# Store a fact
memory.store_fact("echo_agent", "User's name is Alice")

# Retrieve recent interactions
recent = memory.get_recent_interactions("echo_agent", limit=3)

# Get memory summary
summary = memory.get_memory_summary()
print(f"Total interactions: {summary['echo_agent']['interaction_count']}")
```

### Memory-Enabled Crew

The `MemoryEchoCrew` class demonstrates integration:

```python
from crewai_test.memory_echo_crew import MemoryEchoCrew

# Create crew with memory
crew = MemoryEchoCrew()

# Run with automatic memory storage
result = crew.run_with_memory("Remember my name is Bob")

# Memory is automatically persisted
print(crew.get_memory_summary())
```

## Memory Storage Format

The memory store uses JSON format:

```json
{
  "echo_agent": {
    "interactions": [
      {
        "timestamp": "2025-07-28T12:20:36.702849",
        "input": "Hello, my name is Alice",
        "output": "Hello, my name is Alice"
      }
    ],
    "facts": [
      {
        "timestamp": "2025-07-28T12:20:36.702984",
        "fact": "User said: Hello, my name is Alice"
      }
    ]
  }
}
```

## Testing Memory Persistence

### Automated Test

Run the comprehensive memory persistence test:

```bash
cd crewai_test
export $(cat .env | xargs)
PYTHONPATH=src python src/crewai_test/test_memory_persistence.py
```

This test:
1. ✅ Creates initial interactions in Session 1
2. ✅ Simulates application restart with new crew instance
3. ✅ Verifies memory loads correctly in Session 2
4. ✅ Confirms cross-session context awareness
5. ✅ Validates fact and interaction persistence

### Expected Output

```
=== Memory Persistence Test ===

📝 Session 1: Storing initial interactions
📊 Session 1 memory summary: {'echo_agent': {'interaction_count': 3, 'fact_count': 3}}

🔄 Session 2: Creating new crew instance (simulating restart)
📊 Session 2 memory summary: {'echo_agent': {'interaction_count': 3, 'fact_count': 3}}

✅ Memory Persistence Verification:
   ✅ SUCCESS: Memory persistence working correctly!
   ✅ Agent retains information across sessions
```

## Configuration

### Memory Store Settings

```python
# Custom storage location
memory = SimpleMemoryStore("path/to/custom/memory.json")

# Default location (project root)
memory = SimpleMemoryStore()  # Uses "memory_store.json"
```

### CrewAI Memory Settings

```python
@crew
def crew(self) -> Crew:
    return Crew(
        agents=self.agents,
        tasks=self.tasks,
        process=Process.sequential,
        verbose=True,
        memory=True,  # Enable built-in memory
    )
```

## Best Practices

1. **Regular Cleanup**: Periodically clear old memory to prevent unbounded growth
2. **Fact Curation**: Store only meaningful facts to improve context quality
3. **Context Limits**: Limit recent interaction context to prevent token overflow
4. **Backup Strategy**: Regularly backup memory files for production systems
5. **Privacy Considerations**: Sanitize sensitive information before storage

## Memory Lifecycle

1. **Initialization**: Memory store loads existing data from disk
2. **Interaction**: Agent processes input with injected context
3. **Storage**: Interaction and extracted facts saved automatically
4. **Retrieval**: Recent context injected into subsequent interactions
5. **Persistence**: All data survives application restarts

## Troubleshooting

### Common Issues

1. **File Permissions**: Ensure write access to memory storage directory
2. **JSON Corruption**: Backup and restore from valid memory file
3. **Memory Growth**: Implement cleanup strategy for long-running systems
4. **Context Overflow**: Reduce interaction history limit if hitting token limits

### Debug Commands

```python
# Check memory file location
print(memory.storage_path)

# Validate memory contents
summary = memory.get_memory_summary()
print(json.dumps(summary, indent=2))

# Clear corrupted memory
memory.clear_all_memory()
```

## Future Enhancements

- **Vector Embeddings**: Semantic search over memory contents
- **Memory Compression**: Summarize old interactions to save space
- **Multi-Agent Shared Memory**: Cross-agent memory sharing
- **Memory Analytics**: Usage patterns and optimization insights
- **Database Backend**: Scale beyond file-based storage