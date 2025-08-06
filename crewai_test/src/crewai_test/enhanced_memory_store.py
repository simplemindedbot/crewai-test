"""Enhanced memory store with embeddings support for semantic search and cross-agent memory sharing."""

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from .memory_store import SimpleMemoryStore


class EnhancedMemoryStore(SimpleMemoryStore):
    """Enhanced memory store with vector embeddings for semantic search and agent memory sharing."""

    def __init__(
        self,
        storage_path: str = "enhanced_memory_store.json",
        embeddings_path: str = "memory_embeddings.index",
        embedding_model: str = "all-MiniLM-L6-v2",
    ):
        """
        Initialize enhanced memory store with embeddings support.

        Args:
            storage_path: Path to JSON file for structured memory data
            embeddings_path: Path to FAISS index file for vector embeddings
            embedding_model: SentenceTransformers model name for embeddings
        """
        super().__init__(storage_path)

        self.embeddings_path = Path(embeddings_path)
        self.embedding_model = SentenceTransformer(embedding_model)
        self.embedding_dim = 384  # Dimension for all-MiniLM-L6-v2

        # Initialize FAISS index for vector search
        self.index = faiss.IndexFlatIP(
            self.embedding_dim
        )  # Inner product for cosine similarity
        self.text_database: list[str] = (
            []
        )  # Store original texts corresponding to embeddings
        self.metadata_database: list[dict[str, Any]] = (
            []
        )  # Store metadata for each embedding

        self.load_embeddings()

    def load_embeddings(self) -> None:
        """Load existing embeddings index and metadata."""
        if self.embeddings_path.exists():
            try:
                # Load FAISS index
                self.index = faiss.read_index(str(self.embeddings_path))

                # Load text and metadata databases
                metadata_path = self.embeddings_path.with_suffix(".metadata.json")
                if metadata_path.exists():
                    with open(metadata_path) as f:
                        data = json.load(f)
                        self.text_database = data.get("texts", [])
                        self.metadata_database = data.get("metadata", [])

                print(
                    f"✅ Loaded {len(self.text_database)} embeddings from {self.embeddings_path}"
                )
            except Exception as e:
                print(f"⚠️  Could not load embeddings: {e}. Starting fresh.")
                self._initialize_fresh_index()
        else:
            self._initialize_fresh_index()

    def _initialize_fresh_index(self) -> None:
        """Initialize a fresh FAISS index."""
        self.index = faiss.IndexFlatIP(self.embedding_dim)
        self.text_database = []
        self.metadata_database = []

    def save_embeddings(self) -> None:
        """Save embeddings index and metadata to disk."""
        try:
            # Save FAISS index
            faiss.write_index(self.index, str(self.embeddings_path))

            # Save text and metadata databases
            metadata_path = self.embeddings_path.with_suffix(".metadata.json")
            with open(metadata_path, "w") as f:
                json.dump(
                    {"texts": self.text_database, "metadata": self.metadata_database},
                    f,
                    indent=2,
                    default=str,
                )

            print(
                f"💾 Saved {len(self.text_database)} embeddings to {self.embeddings_path}"
            )
        except Exception as e:
            print(f"❌ Error saving embeddings: {e}")

    def add_to_vector_store(self, text: str, metadata: dict[str, Any]) -> None:
        """
        Add text to vector store with embeddings.

        Args:
            text: Text to embed and store
            metadata: Associated metadata (agent_name, timestamp, type, etc.)
        """
        try:
            # Generate embedding
            embedding = self.embedding_model.encode([text], normalize_embeddings=True)
            embedding = embedding.astype(np.float32)

            # Add to FAISS index
            self.index.add(embedding)

            # Add to databases
            self.text_database.append(text)
            self.metadata_database.append(metadata)

            # Save periodically
            if len(self.text_database) % 10 == 0:
                self.save_embeddings()

        except Exception as e:
            print(f"❌ Error adding to vector store: {e}")

    def semantic_search(
        self,
        query: str,
        top_k: int = 5,
        agent_filter: str | None = None,
        min_similarity: float = 0.3,
    ) -> list[dict[str, Any]]:
        """
        Perform semantic search across all stored memories.

        Args:
            query: Search query text
            top_k: Number of top results to return
            agent_filter: Optional agent name to filter results
            min_similarity: Minimum cosine similarity threshold

        Returns:
            List of search results with text, metadata, and similarity scores
        """
        if len(self.text_database) == 0:
            return []

        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(
                [query], normalize_embeddings=True
            )
            query_embedding = query_embedding.astype(np.float32)

            # Search FAISS index
            scores, indices = self.index.search(
                query_embedding, min(top_k * 2, len(self.text_database))
            )

            results = []
            for i, (score, idx) in enumerate(zip(scores[0], indices[0], strict=False)):
                if score < min_similarity:
                    continue

                metadata = self.metadata_database[idx]

                # Apply agent filter if specified
                if agent_filter and metadata.get("agent_name") != agent_filter:
                    continue

                results.append(
                    {
                        "text": self.text_database[idx],
                        "metadata": metadata,
                        "similarity": float(score),
                        "rank": i + 1,
                    }
                )

                if len(results) >= top_k:
                    break

            return results

        except Exception as e:
            print(f"❌ Error in semantic search: {e}")
            return []

    def store_interaction(
        self, agent_name: str, input_message: str, output_message: str
    ) -> None:
        """Enhanced interaction storage with embeddings."""
        # Call parent method for structured storage
        super().store_interaction(agent_name, input_message, output_message)

        # Add to vector store for semantic search
        interaction_text = (
            f"Agent: {agent_name}\nInput: {input_message}\nOutput: {output_message}"
        )
        metadata = {
            "agent_name": agent_name,
            "type": "interaction",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "input": input_message,
            "output": (
                output_message[:200] + "..."
                if len(output_message) > 200
                else output_message
            ),
        }
        self.add_to_vector_store(interaction_text, metadata)

    def store_fact(self, agent_name: str, fact: str) -> None:
        """Enhanced fact storage with embeddings."""
        # Call parent method for structured storage
        super().store_fact(agent_name, fact)

        # Add to vector store for semantic search
        fact_text = f"Agent: {agent_name}\nFact: {fact}"
        metadata = {
            "agent_name": agent_name,
            "type": "fact",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "fact": fact,
        }
        self.add_to_vector_store(fact_text, metadata)

    def get_relevant_context(
        self, agent_name: str, query: str, context_limit: int = 5
    ) -> list[dict[str, Any]]:
        """
        Get relevant context for an agent based on semantic similarity.

        Args:
            agent_name: Name of the agent requesting context
            query: Current query/task for finding relevant context
            context_limit: Maximum number of context items to return

        Returns:
            List of relevant context items from all agents
        """
        # Search for relevant memories across all agents
        all_results = self.semantic_search(query, top_k=context_limit * 2)

        # Also include agent-specific memories
        agent_results = self.semantic_search(
            query, top_k=context_limit, agent_filter=agent_name
        )

        # Combine and deduplicate
        seen_texts = set()
        combined_results = []

        # Prioritize agent-specific results
        for result in agent_results:
            if result["text"] not in seen_texts:
                result["source"] = "agent_specific"
                combined_results.append(result)
                seen_texts.add(result["text"])

        # Add cross-agent results
        for result in all_results:
            if (
                result["text"] not in seen_texts
                and len(combined_results) < context_limit
            ):
                result["source"] = "cross_agent"
                combined_results.append(result)
                seen_texts.add(result["text"])

        return combined_results[:context_limit]

    def get_cross_agent_insights(
        self, topic: str, exclude_agent: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Get insights from other agents on a specific topic.

        Args:
            topic: Topic to search for insights
            exclude_agent: Agent name to exclude from results

        Returns:
            List of relevant insights from other agents
        """
        results = self.semantic_search(topic, top_k=10)

        # Filter out specified agent
        if exclude_agent:
            results = [
                r for r in results if r["metadata"].get("agent_name") != exclude_agent
            ]

        return results[:5]

    def get_memory_analytics(self) -> dict[str, Any]:
        """Get analytics about the memory store."""
        analytics = super().get_memory_summary()

        # Add embeddings analytics
        analytics["embeddings"] = {
            "total_embeddings": len(self.text_database),
            "embedding_dimension": self.embedding_dim,
            "model": "all-MiniLM-L6-v2",
        }

        # Agent distribution in embeddings
        agent_distribution = {}
        for metadata in self.metadata_database:
            agent_name = metadata.get("agent_name", "unknown")
            agent_distribution[agent_name] = agent_distribution.get(agent_name, 0) + 1

        analytics["embeddings"]["agent_distribution"] = agent_distribution

        return analytics

    def __del__(self):
        """Ensure embeddings are saved when object is destroyed."""
        try:
            if hasattr(self, "index") and len(self.text_database) > 0:
                self.save_embeddings()
        except Exception:
            pass  # Ignore errors during cleanup
