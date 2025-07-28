"""Enhanced echo crew with explicit memory persistence."""

from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task

from .memory_store import SimpleMemoryStore


@CrewBase
class MemoryEchoCrew:
    """Echo crew with explicit memory persistence functionality."""

    agents_config = "config/agents_echo.yaml"
    tasks_config = "config/tasks_echo.yaml"

    agents: list[BaseAgent]
    tasks: list[Task]

    def __init__(self):
        super().__init__()
        self.memory_store = SimpleMemoryStore("echo_agent_memory.json")

    @agent
    def echo_agent(self) -> Agent:
        """Create an echo agent with memory capabilities."""
        return Agent(
            config=self.agents_config["echo_agent"],  # type: ignore[index]
            verbose=True,
        )

    @task
    def echo_task(self) -> Task:
        """Create an echo task that uses memory."""
        return Task(
            config=self.tasks_config["echo_task"],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the memory-enabled Echo crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,  # Enable CrewAI's built-in memory
        )

    def run_with_memory(self, input_message: str) -> str:
        """Run the crew and store the interaction in memory."""
        # Store previous interactions context
        recent_interactions = self.memory_store.get_recent_interactions("echo_agent", limit=3)

        # Add context to input if there are previous interactions
        context_input = input_message
        if recent_interactions:
            context_lines = ["Previous interactions:"]
            for interaction in recent_interactions:
                context_lines.append(f"- Input: {interaction['input']}, Output: {interaction['output']}")
            context_lines.append(f"Current input: {input_message}")
            context_input = "\n".join(context_lines)

        # Run the crew
        inputs = {
            "input_message": context_input,
        }

        result = self.crew().kickoff(inputs=inputs)
        output_message = str(result)

        # Store the interaction
        self.memory_store.store_interaction("echo_agent", input_message, output_message)

        # Store as a fact if it's something worth remembering
        if len(input_message) > 5:  # Simple heuristic
            self.memory_store.store_fact("echo_agent", f"User said: {input_message}")

        return output_message

    def get_memory_summary(self) -> dict:
        """Get a summary of the agent's memory."""
        return self.memory_store.get_memory_summary()

    def clear_memory(self) -> None:
        """Clear the agent's memory."""
        self.memory_store.clear_all_memory()
