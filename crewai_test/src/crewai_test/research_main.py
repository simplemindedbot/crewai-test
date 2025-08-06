"""Main entry point for the multi-agent research crew."""

import sys

from .research_crew import ResearchCrew


def run_research_crew():
    """Run the multi-agent research crew with command line topic input."""

    # Get topic from command line or use default
    topic = (
        sys.argv[1] if len(sys.argv) > 1 else "artificial intelligence in healthcare"
    )
    current_year = 2024

    print(f"🔍 Starting multi-agent research on: {topic}")
    print(f"📅 Research year context: {current_year}")
    print("=" * 50)

    try:
        # Initialize the research crew
        crew = ResearchCrew()

        # Execute the research workflow
        result = crew.run_research(topic, current_year)

        print("\n" + "=" * 50)
        print("🎯 Research Workflow Complete!")
        print("=" * 50)
        print(f"📋 Topic: {topic}")
        print("📝 Report saved to: research_report.md")
        print(f"🧠 Memory interactions stored: {crew.get_memory_summary()}")

        # Display abbreviated result
        print("\n📄 Research Summary:")
        print("-" * 30)
        if len(result) > 500:
            print(f"{result[:500]}...")
            print("\n[Full report available in research_report.md]")
        else:
            print(result)

    except Exception as e:
        print(f"❌ Error during research workflow: {e}")
        return False

    return True


if __name__ == "__main__":
    success = run_research_crew()
    sys.exit(0 if success else 1)
