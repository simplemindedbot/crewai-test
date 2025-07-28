from crewai import Agent, Crew, Process, Task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.project import CrewBase, agent, crew, task


@CrewBase
class EchoCrew:
    """Minimal echo crew for Sprint 1 milestone."""

    agents_config = "config/agents_echo.yaml"
    tasks_config = "config/tasks_echo.yaml"

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def echo_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["echo_agent"],  # type: ignore[index]
            verbose=True,
        )

    @task
    def echo_task(self) -> Task:
        return Task(
            config=self.tasks_config["echo_task"],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the minimal Echo crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
