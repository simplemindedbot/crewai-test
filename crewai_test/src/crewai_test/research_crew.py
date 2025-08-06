"""Multi-agent research crew implementing Researcher → Summarizer → Validator → Coordinator flow."""

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from .enhanced_memory_store import EnhancedMemoryStore


@CrewBase
class ResearchCrew:
    """Multi-agent research crew with persistent memory capabilities."""

    agents_config = "config/agents_research.yaml"
    tasks_config = "config/tasks_research.yaml"

    agents: list[BaseAgent]
    tasks: list[Task]

    def __init__(self):
        super().__init__()
        # Initialize enhanced memory store with embeddings for cross-agent memory
        self.memory_store = EnhancedMemoryStore(
            "research_crew_memory.json",
            "research_crew_embeddings.index"
        )

    @agent
    def researcher_agent(self) -> Agent:
        """Primary research agent responsible for gathering comprehensive information."""
        return Agent(
            config=self.agents_config["researcher_agent"],
            verbose=True,
            memory=True,
        )

    @agent
    def summarizer_agent(self) -> Agent:
        """Content summarization specialist for distilling research findings."""
        return Agent(
            config=self.agents_config["summarizer_agent"],
            verbose=True,
            memory=True,
        )

    @agent
    def validator_agent(self) -> Agent:
        """Fact-checking and validation specialist ensuring information quality."""
        return Agent(
            config=self.agents_config["validator_agent"],
            verbose=True,
            memory=True,
        )

    @agent
    def coordinator_agent(self) -> Agent:
        """Research coordinator synthesizing all outputs into final reports."""
        return Agent(
            config=self.agents_config["coordinator_agent"],
            verbose=True,
            memory=True,
        )

    @task
    def research_task(self) -> Task:
        """Comprehensive research task executed by researcher_agent."""
        return Task(
            config=self.tasks_config["research_task"],
        )

    @task
    def summarize_task(self) -> Task:
        """Content summarization task dependent on research completion."""
        return Task(
            config=self.tasks_config["summarize_task"],
            dependencies=[self.research_task],  # Depends on research completion
        )

    @task
    def validate_task(self) -> Task:
        """Validation task dependent on summarization completion."""
        return Task(
            config=self.tasks_config["validate_task"],
            dependencies=[self.summarize_task],  # Depends on summary completion
        )

    @task
    def coordinate_task(self) -> Task:
        """Final coordination task dependent on validation completion."""
        return Task(
            config=self.tasks_config["coordinate_task"],
            dependencies=[self.validate_task],  # Depends on validation completion
            output_file="research_report.md",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the multi-agent research crew with sequential workflow."""
        return Crew(
            agents=self.agents,  # All four agents: researcher, summarizer, validator, coordinator
            tasks=self.tasks,    # All four tasks with proper dependencies
            process=Process.sequential,
            verbose=True,
            memory=True,  # Enable CrewAI's built-in memory system
        )

    def run_research(self, topic: str, current_year: int = 2024) -> str:
        """Execute the complete research workflow with memory persistence."""

        # Inject previous research context if available
        previous_context = self._get_research_context(topic)

        inputs = {
            "topic": topic,
            "current_year": current_year,
        }

        # Add context if we have previous research on this topic
        if previous_context:
            context_summary = f"\n\nPrevious research context:\n{previous_context}"
            inputs["context"] = context_summary

        # Execute the crew workflow
        result = self.crew().kickoff(inputs=inputs)
        output = str(result)

        # Store the research interaction in memory
        self.memory_store.store_interaction(
            "research_crew",
            f"Research topic: {topic}",
            output
        )

        # Extract and store key facts
        self._extract_and_store_facts(topic, output)

        return output

    def _get_research_context(self, topic: str) -> str:
        """Retrieve previous research context using semantic search."""
        # Use semantic search to find relevant context
        relevant_memories = self.memory_store.get_relevant_context(
            "research_crew",
            topic,
            context_limit=3
        )

        if not relevant_memories:
            return ""

        context_lines = ["Previous relevant research context:"]
        for memory in relevant_memories:
            source_type = memory.get('source', 'unknown')
            similarity = memory.get('similarity', 0.0)
            metadata = memory.get('metadata', {})

            # Format context based on type
            if metadata.get('type') == 'fact':
                context_lines.append(
                    f"- [{source_type}, {similarity:.2f}] Fact: {metadata.get('fact', '')}"
                )
            elif metadata.get('type') == 'interaction':
                context_lines.append(
                    f"- [{source_type}, {similarity:.2f}] Previous research: {metadata.get('input', '')}"
                )

        return "\n".join(context_lines)

    def _extract_and_store_facts(self, topic: str, output: str) -> None:
        """Extract and store key facts from the research output."""
        # Simple fact extraction - in production this could be more sophisticated
        if "key findings" in output.lower():
            fact = f"Research completed on {topic} with comprehensive findings"
            self.memory_store.store_fact("research_crew", fact)

        if "sources" in output.lower() or "references" in output.lower():
            fact = f"Authoritative sources identified for {topic} research"
            self.memory_store.store_fact("research_crew", fact)

    def get_memory_summary(self) -> dict:
        """Get a comprehensive summary of the crew's memory state with analytics."""
        return self.memory_store.get_memory_analytics()
