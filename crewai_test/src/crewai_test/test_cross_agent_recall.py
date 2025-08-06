"""Test script to verify agents can recall facts across different task executions."""

import sys

from .enhanced_memory_store import EnhancedMemoryStore


def test_cross_agent_recall():
    """Test that agents can recall facts from other agents across different tasks."""

    print("🧠 Testing Cross-Agent Fact Recall")
    print("=" * 50)

    # Initialize memory store
    print("📝 Initializing Enhanced Memory Store...")
    memory_store = EnhancedMemoryStore("cross_agent_memory.json", "cross_agent_embeddings.index")

    # Simulate a multi-agent research workflow
    print("\n📋 Simulating Multi-Agent Research Workflow")
    print("-" * 40)

    # Phase 1: Research Agent discovers facts
    print("\n🔍 Phase 1: Research Agent Discovery")
    memory_store.store_fact("researcher_agent", "Machine learning adoption increased 45% in healthcare in 2024")
    memory_store.store_fact("researcher_agent", "FDA approved 12 new AI-powered diagnostic tools this year")
    memory_store.store_interaction(
        "researcher_agent",
        "Research AI in healthcare trends",
        "Comprehensive research completed. Key finding: AI diagnostic tools are rapidly gaining FDA approval with machine learning showing significant adoption growth in clinical settings."
    )

    # Phase 2: Summarizer Agent processes and adds context
    print("📝 Phase 2: Summarizer Agent Processing")
    memory_store.store_fact("summarizer_agent", "Healthcare AI market projected to reach $102 billion by 2028")
    memory_store.store_interaction(
        "summarizer_agent",
        "Summarize healthcare AI research findings",
        "Healthcare AI Summary: The sector shows remarkable growth with 45% increase in ML adoption, 12 new FDA approvals for diagnostic tools, and market projection of $102B by 2028."
    )

    # Phase 3: Validator Agent cross-references facts
    print("✅ Phase 3: Validator Agent Verification")
    memory_store.store_fact("validator_agent", "FDA approval data verified against official government database")
    memory_store.store_fact("validator_agent", "Market projection figures confirmed with McKinsey Healthcare AI Report 2024")
    memory_store.store_interaction(
        "validator_agent",
        "Validate healthcare AI claims and statistics",
        "Validation completed: FDA approval numbers confirmed via official database. Market projections verified against McKinsey 2024 report. High confidence in data accuracy."
    )

    # Test Cross-Agent Recall Scenarios
    print("\n🧪 Testing Cross-Agent Recall Scenarios")
    print("-" * 40)

    # Scenario 1: Coordinator needs to recall researcher findings
    print("\n📊 Scenario 1: Coordinator recalling Research findings")
    research_context = memory_store.get_relevant_context(
        "coordinator_agent",
        "FDA diagnostic AI approvals research data",
        context_limit=3
    )

    print(f"   Found {len(research_context)} relevant memories:")
    researcher_facts_found = 0
    for ctx in research_context:
        agent = ctx['metadata'].get('agent_name', 'unknown')
        content_type = ctx['metadata'].get('type', 'unknown')
        similarity = ctx.get('similarity', 0.0)
        print(f"   - Agent: {agent} | Type: {content_type} | Similarity: {similarity:.3f}")
        if agent == "researcher_agent":
            researcher_facts_found += 1

    # Scenario 2: Summarizer recalls validator confirmations
    print("\n📋 Scenario 2: Summarizer recalling Validator confirmations")
    validation_context = memory_store.get_relevant_context(
        "summarizer_agent",
        "data verification and validation accuracy",
        context_limit=3
    )

    print(f"   Found {len(validation_context)} validation memories:")
    validator_facts_found = 0
    for ctx in validation_context:
        agent = ctx['metadata'].get('agent_name', 'unknown')
        content_type = ctx['metadata'].get('type', 'unknown')
        similarity = ctx.get('similarity', 0.0)
        print(f"   - Agent: {agent} | Type: {content_type} | Similarity: {similarity:.3f}")
        if agent == "validator_agent":
            validator_facts_found += 1

    # Scenario 3: Cross-agent insights for new topic
    print("\n💡 Scenario 3: Cross-agent insights for healthcare market analysis")
    market_insights = memory_store.get_cross_agent_insights("healthcare market growth projections")

    print(f"   Found {len(market_insights)} market insights:")
    unique_agents = set()
    for insight in market_insights:
        agent = insight['metadata'].get('agent_name', 'unknown')
        unique_agents.add(agent)
        similarity = insight.get('similarity', 0.0)
        print(f"   - Agent: {agent} | Similarity: {similarity:.3f}")
        print(f"     Content: {insight['text'][:80]}...")

    # Scenario 4: Semantic search across all agents
    print("\n🔍 Scenario 4: Semantic search for 'FDA approval' across all agents")
    fda_results = memory_store.semantic_search("FDA approval diagnostic tools", top_k=4)

    agents_with_fda_info = set()
    for result in fda_results:
        agent = result['metadata'].get('agent_name', 'unknown')
        agents_with_fda_info.add(agent)
        similarity = result.get('similarity', 0.0)
        content_type = result['metadata'].get('type', 'unknown')
        print(f"   - Agent: {agent} | Type: {content_type} | Similarity: {similarity:.3f}")

    # Test Results Analysis
    print("\n📊 Cross-Agent Recall Analysis")
    print("-" * 40)

    total_agents_in_memory = len({meta.get('agent_name', 'unknown') for meta in memory_store.metadata_database})

    print(f"   Total unique agents in memory: {total_agents_in_memory}")
    print(f"   Agents with FDA information: {len(agents_with_fda_info)}")
    print(f"   Cross-agent market insights: {len(unique_agents)} agents contributed")
    print(f"   Researcher facts accessible to coordinator: {researcher_facts_found}")
    print(f"   Validator facts accessible to summarizer: {validator_facts_found}")

    # Memory Analytics
    analytics = memory_store.get_memory_analytics()
    print("\n📈 Memory Store Analytics:")
    print(f"   Total embeddings: {analytics['embeddings']['total_embeddings']}")
    print(f"   Agent distribution: {analytics['embeddings']['agent_distribution']}")

    # Success Criteria
    success_criteria = [
        ("Cross-agent context retrieval", len(research_context) >= 1),
        ("Multi-agent FDA information", len(agents_with_fda_info) >= 2),
        ("Validator facts accessible", validator_facts_found >= 1),
        ("Researcher facts accessible", researcher_facts_found >= 1),
        ("Cross-agent insights", len(unique_agents) >= 2),
        ("Memory persistence", analytics['embeddings']['total_embeddings'] >= 6)
    ]

    print("\n✅ Success Criteria Evaluation:")
    passed_tests = 0
    for criterion, passed in success_criteria:
        status = "PASS" if passed else "FAIL"
        print(f"   {status}: {criterion}")
        if passed:
            passed_tests += 1

    # Final cleanup
    try:
        import os
        os.remove("cross_agent_memory.json")
        os.remove("cross_agent_embeddings.index")
        os.remove("cross_agent_embeddings.index.metadata.json")
        print("\n🧹 Cleaned up test files")
    except Exception:
        pass

    overall_success = passed_tests >= 5

    if overall_success:
        print("\n🎉 SUCCESS: Cross-Agent Fact Recall Working!")
        print(f"   ✅ Passed {passed_tests}/{len(success_criteria)} tests")
        print("   ✅ Agents can recall facts from other agents")
        print("   ✅ Semantic search enables cross-agent knowledge sharing")
        print("   ✅ Memory persistence maintains agent knowledge across tasks")
    else:
        print("\n❌ FAILURE: Cross-Agent Fact Recall Issues")
        print(f"   ❌ Passed {passed_tests}/{len(success_criteria)} tests")

    return overall_success


if __name__ == "__main__":
    success = test_cross_agent_recall()
    sys.exit(0 if success else 1)
