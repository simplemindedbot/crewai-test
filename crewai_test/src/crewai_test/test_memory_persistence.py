#!/usr/bin/env python
"""
Test script to demonstrate memory persistence across sessions.
"""
import sys
import warnings

from crewai_test.memory_echo_crew import MemoryEchoCrew

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def test_memory_persistence():
    """Test that memory persists across different crew instances."""
    print("=== Memory Persistence Test ===\n")

    # Test 1: First session - store some interactions
    print("📝 Session 1: Storing initial interactions")
    crew1 = MemoryEchoCrew()

    # Clear previous memory for clean test
    crew1.clear_memory()

    # Store some test interactions
    result1 = crew1.run_with_memory("Hello, my name is Alice")
    print("Input: Hello, my name is Alice")
    print(f"Output: {result1}\n")

    result2 = crew1.run_with_memory("I like programming in Python")
    print("Input: I like programming in Python")
    print(f"Output: {result2}\n")

    result3 = crew1.run_with_memory("What's the weather like?")
    print("Input: What's the weather like?")
    print(f"Output: {result3}\n")

    # Show memory summary
    memory_summary = crew1.get_memory_summary()
    print(f"📊 Session 1 memory summary: {memory_summary}\n")

    # Test 2: Second session - new crew instance should recall previous interactions
    print("🔄 Session 2: Creating new crew instance (simulating restart)")
    crew2 = MemoryEchoCrew()  # New instance, should load existing memory

    # Check if memory was loaded
    memory_summary2 = crew2.get_memory_summary()
    print(
        f"📊 Session 2 memory summary (should show previous data): {memory_summary2}\n"
    )

    # Test interaction with memory context
    result4 = crew2.run_with_memory("Do you remember my name?")
    print("Input: Do you remember my name?")
    print(f"Output: {result4}\n")

    # Test 3: Verify memory persisted
    print("✅ Memory Persistence Verification:")

    # Check that we have interactions from both sessions
    final_memory = crew2.get_memory_summary()
    echo_agent_data = final_memory.get("echo_agent", {})
    interaction_count = echo_agent_data.get("interaction_count", 0)
    fact_count = echo_agent_data.get("fact_count", 0)

    print(f"   - Total interactions stored: {interaction_count}")
    print(f"   - Total facts stored: {fact_count}")
    print(
        f"   - Last interaction time: {echo_agent_data.get('last_interaction', 'None')}"
    )

    # Verify success criteria
    if interaction_count >= 4 and fact_count >= 3:
        print("   ✅ SUCCESS: Memory persistence working correctly!")
        print("   ✅ Agent retains information across sessions")
    else:
        print("   ❌ FAILURE: Memory persistence not working as expected")
        print("   Expected: ≥4 interactions, ≥3 facts")
        print(f"   Got: {interaction_count} interactions, {fact_count} facts")

    # Test 4: Show detailed memory
    print("\n📚 Detailed Memory Contents:")
    recent_interactions = crew2.memory_store.get_recent_interactions(
        "echo_agent", limit=10
    )
    for i, interaction in enumerate(recent_interactions, 1):
        print(f"   {i}. [{interaction['timestamp']}]")
        print(f"      Input: {interaction['input']}")
        print(f"      Output: {interaction['output'][:100]}...")

    print("\n🧠 Stored Facts:")
    facts = crew2.memory_store.get_agent_facts("echo_agent")
    for i, fact in enumerate(facts, 1):
        print(f"   {i}. [{fact['timestamp']}] {fact['fact']}")

    return interaction_count >= 4 and fact_count >= 3


if __name__ == "__main__":
    success = test_memory_persistence()
    sys.exit(0 if success else 1)
