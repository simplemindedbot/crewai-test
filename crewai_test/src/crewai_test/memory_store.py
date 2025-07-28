"""Simple file-based memory store for persistent agent memory."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any


class SimpleMemoryStore:
    """A basic file-based memory store for agent persistence."""

    def __init__(self, storage_path: str = "memory_store.json"):
        """Initialize the memory store with a storage file path."""
        self.storage_path = Path(storage_path)
        self.memory: dict[str, Any] = {}
        self.load_memory()

    def load_memory(self) -> None:
        """Load memory from the storage file."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path) as f:
                    self.memory = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.memory = {}

    def save_memory(self) -> None:
        """Save current memory to the storage file."""
        # Ensure parent directory exists
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)

        with open(self.storage_path, 'w') as f:
            json.dump(self.memory, f, indent=2, default=str)

    def store_interaction(self, agent_name: str, input_message: str, output_message: str) -> None:
        """Store an agent interaction in memory."""
        if agent_name not in self.memory:
            self.memory[agent_name] = {"interactions": [], "facts": []}

        interaction = {
            "timestamp": datetime.now().isoformat(),
            "input": input_message,
            "output": output_message
        }

        self.memory[agent_name]["interactions"].append(interaction)
        self.save_memory()

    def store_fact(self, agent_name: str, fact: str) -> None:
        """Store a learned fact for an agent."""
        if agent_name not in self.memory:
            self.memory[agent_name] = {"interactions": [], "facts": []}

        fact_entry = {
            "timestamp": datetime.now().isoformat(),
            "fact": fact
        }

        self.memory[agent_name]["facts"].append(fact_entry)
        self.save_memory()

    def get_agent_history(self, agent_name: str) -> list[dict[str, Any]]:
        """Get all interactions for a specific agent."""
        if agent_name in self.memory:
            return self.memory[agent_name]["interactions"]
        return []

    def get_agent_facts(self, agent_name: str) -> list[dict[str, Any]]:
        """Get all stored facts for a specific agent."""
        if agent_name in self.memory:
            return self.memory[agent_name]["facts"]
        return []

    def get_recent_interactions(self, agent_name: str, limit: int = 5) -> list[dict[str, Any]]:
        """Get the most recent interactions for an agent."""
        interactions = self.get_agent_history(agent_name)
        return interactions[-limit:] if interactions else []

    def clear_agent_memory(self, agent_name: str) -> None:
        """Clear all memory for a specific agent."""
        if agent_name in self.memory:
            del self.memory[agent_name]
            self.save_memory()

    def clear_all_memory(self) -> None:
        """Clear all stored memory."""
        self.memory = {}
        if self.storage_path.exists():
            self.storage_path.unlink()

    def get_memory_summary(self) -> dict[str, Any]:
        """Get a summary of stored memory."""
        summary = {}
        for agent_name, data in self.memory.items():
            summary[agent_name] = {
                "interaction_count": len(data.get("interactions", [])),
                "fact_count": len(data.get("facts", [])),
                "last_interaction": data.get("interactions", [{}])[-1].get("timestamp") if data.get("interactions") else None
            }
        return summary
