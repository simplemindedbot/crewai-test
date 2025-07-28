"""Test cases for Echo Crew functionality."""

import pytest
from crewai_test.echo_crew import EchoCrew


class TestEchoCrew:
    """Test cases for EchoCrew."""

    def test_echo_crew_initialization(self):
        """Test that echo crew can be initialized."""
        crew = EchoCrew()
        assert crew is not None
        
    def test_echo_crew_has_agents(self):
        """Test that echo crew has the expected agents."""
        crew = EchoCrew()
        agents = crew.crew().agents
        assert len(agents) == 1
        assert agents[0].role == "Echo Agent"
        
    def test_echo_crew_has_tasks(self):
        """Test that echo crew has the expected tasks.""" 
        crew = EchoCrew()
        tasks = crew.crew().tasks
        assert len(tasks) == 1
        assert "echo back the input message" in tasks[0].description.lower()
        
    def test_echo_crew_agent_configuration(self):
        """Test that echo agent has correct configuration."""
        crew = EchoCrew()
        agent = crew.echo_agent()
        assert agent.role == "Echo Agent"
        assert "echo back" in agent.goal.lower()
        assert "echo agent" in agent.backstory.lower()
        
    def test_echo_crew_task_configuration(self):
        """Test that echo task has correct configuration."""
        crew = EchoCrew()
        task = crew.echo_task()
        assert "echo back the input message" in task.description.lower()
        assert "exact input message" in task.expected_output.lower()