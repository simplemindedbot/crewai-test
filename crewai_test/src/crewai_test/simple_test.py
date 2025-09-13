#!/usr/bin/env python
"""
Simple test to validate CrewAI installation and basic functionality
without requiring external API keys.
"""
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from crewai import Agent, Crew, Process, Task
    from crewai.project import CrewBase
    print("✅ CrewAI import successful")
    
    # Test basic agent creation
    test_agent = Agent(
        role="Test Agent",
        goal="Test basic functionality",
        backstory="Simple test agent for validation",
        verbose=False,
        llm=None  # Will use default but won't execute
    )
    print("✅ Agent creation successful")
    
    # Test basic task creation  
    test_task = Task(
        description="Simple test task",
        expected_output="Test output",
        agent=test_agent
    )
    print("✅ Task creation successful")
    
    # Test crew creation (without execution)
    test_crew = Crew(
        agents=[test_agent],
        tasks=[test_task], 
        process=Process.sequential,
        verbose=False
    )
    print("✅ Crew creation successful")
    
    print("\n🎉 Sprint 1 Milestone: CrewAI installation and basic functionality validated!")
    print("✅ All core CrewAI components can be imported and instantiated")
    print("⚠️  LLM execution requires API key configuration for full testing")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)