#!/usr/bin/env python
"""
Echo crew main entry point for Sprint 1 testing.
"""
import sys
import warnings
from datetime import datetime

from crewai_test.echo_crew import EchoCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run_echo():
    """
    Run the echo crew with a simple test message.
    """
    # Get message from command line or use default
    test_message = sys.argv[1] if len(sys.argv) > 1 else "Hello, Echo Crew!"
    
    inputs = {
        "input_message": test_message,
        "current_year": str(datetime.now().year)
    }

    try:
        result = EchoCrew().crew().kickoff(inputs=inputs)
        print(f"\n=== Echo Crew Result ===")
        print(f"Input: {test_message}")
        print(f"Output: {result}")
        return result
    except Exception as e:
        raise Exception(f"An error occurred while running the echo crew: {e}") from e


if __name__ == "__main__":
    run_echo()