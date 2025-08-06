"""Test cases for CrewAI crew functionality."""

import pytest
from crewai_test.crew import CrewaiTest


class TestCrewaiTest:
    """Test cases for CrewaiTest."""

    def test_crew_initialization(self):
        """Test that crew can be initialized."""
        crew = CrewaiTest()
        assert crew is not None
        
    def test_crew_has_agents(self):
        """Test that crew has the expected agents."""
        crew = CrewaiTest()
        agents = crew.crew().agents
        assert len(agents) >= 1
        
    def test_crew_has_tasks(self):
        """Test that crew has the expected tasks.""" 
        crew = CrewaiTest()
        tasks = crew.crew().tasks
        assert len(tasks) >= 1