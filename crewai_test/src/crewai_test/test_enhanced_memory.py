"""Test script for enhanced memory store with embeddings and cross-agent memory sharing."""

import os
import sys

from .enhanced_memory_store import EnhancedMemoryStore


def test_enhanced_memory():
    """Test enhanced memory store functionality including embeddings and semantic search."""

    print("🧠 Testing Enhanced Memory Store with Embeddings")
    print("=" * 60)

    # Initialize enhanced memory store
    print("📝 Initializing Enhanced Memory Store...")
    memory_store = EnhancedMemoryStore("test_enhanced_memory.json", "test_embeddings.index")

    # Test 1: Store interactions from different agents
    print("\n📋 Test 1: Storing interactions from multiple agents")

    # Simulate researcher agent interactions
    memory_store.store_interaction(
        "researcher_agent",
        "Research artificial intelligence trends in 2024",
        "Found key trends: Large Language Models, Multimodal AI, AI Safety regulations, and Edge AI deployment. Key sources include MIT Technology Review, Stanford AI Index, and recent OpenAI publications."
    )

    memory_store.store_interaction(
        "summarizer_agent",
        "Summarize AI trends research findings",
        "Key AI trends for 2024: 1) LLMs becoming mainstream, 2) Multimodal AI integration, 3) Increased AI safety focus, 4) Edge computing adoption for AI workloads."
    )

    memory_store.store_interaction(
        "validator_agent",
        "Validate AI trends claims and sources",
        "Verified: MIT Technology Review and Stanford AI Index are authoritative sources. Cross-referenced statistics with additional academic papers. High confidence in trend accuracy."
    )

    print("✅ Stored interactions from 3 agents")

    # Test 2: Store facts
    print("\n📋 Test 2: Storing facts from agents")

    memory_store.store_fact("researcher_agent", "Large Language Models showed 340% growth in enterprise adoption in 2024")
    memory_store.store_fact("validator_agent", "MIT Technology Review ranked as top-tier AI publication with 95% accuracy rating")
    memory_store.store_fact("coordinator_agent", "Research workflow completed with high confidence validation scores")

    print("✅ Stored facts from 3 agents")

    # Test 3: Semantic search across agents
    print("\n📋 Test 3: Semantic search across all agents")

    # Search for AI-related content
    ai_results = memory_store.semantic_search("artificial intelligence trends", top_k=3)
    print(f"🔍 Found {len(ai_results)} AI-related memories:")

    for i, result in enumerate(ai_results, 1):
        metadata = result['metadata']
        print(f"   {i}. Agent: {metadata.get('agent_name', 'unknown')}")
        print(f"      Type: {metadata.get('type', 'unknown')}")
        print(f"      Similarity: {result['similarity']:.3f}")
        print(f"      Content: {result['text'][:100]}...")
        print()

    # Test 4: Cross-agent context retrieval
    print("📋 Test 4: Cross-agent context retrieval")

    context = memory_store.get_relevant_context("coordinator_agent", "machine learning validation", context_limit=3)
    print(f"📚 Found {len(context)} relevant context items for coordinator:")

    for i, ctx in enumerate(context, 1):
        source = ctx.get('source', 'unknown')
        similarity = ctx.get('similarity', 0.0)
        agent = ctx['metadata'].get('agent_name', 'unknown')
        print(f"   {i}. [{source}] Agent: {agent} (similarity: {similarity:.3f})")
        print(f"      Content: {ctx['text'][:80]}...")
        print()

    # Test 5: Cross-agent insights
    print("📋 Test 5: Cross-agent insights")

    insights = memory_store.get_cross_agent_insights("validation sources", exclude_agent="validator_agent")
    print(f"💡 Found {len(insights)} insights from other agents about validation:")

    for i, insight in enumerate(insights, 1):
        agent = insight['metadata'].get('agent_name', 'unknown')
        similarity = insight.get('similarity', 0.0)
        print(f"   {i}. Agent: {agent} (similarity: {similarity:.3f})")
        print(f"      Insight: {insight['text'][:80]}...")
        print()

    # Test 6: Memory analytics
    print("📋 Test 6: Memory analytics")

    analytics = memory_store.get_memory_analytics()
    print("📊 Memory Analytics:")
    print(f"   Total interactions: {analytics.get('total_interactions', 0)}")
    print(f"   Total facts: {analytics.get('total_facts', 0)}")
    print(f"   Total embeddings: {analytics['embeddings']['total_embeddings']}")
    print(f"   Embedding dimension: {analytics['embeddings']['embedding_dimension']}")

    agent_dist = analytics['embeddings']['agent_distribution']
    print(f"   Agent distribution: {agent_dist}")

    # Test 7: Verify persistence
    print("\n📋 Test 7: Testing persistence")

    print("💾 Saving current state...")
    memory_store.save_embeddings()

    print("🔄 Creating new instance to test loading...")
    memory_store2 = EnhancedMemoryStore("test_enhanced_memory.json", "test_embeddings.index")

    # Test search on reloaded instance
    search_results = memory_store2.semantic_search("artificial intelligence", top_k=2)
    print(f"🔍 Reloaded instance found {len(search_results)} results")

    # Test final analytics
    final_analytics = memory_store2.get_memory_analytics()
    embeddings_count = final_analytics['embeddings']['total_embeddings']

    print("\n🎯 Final Results:")
    print(f"   ✅ Embeddings persistence: {embeddings_count} embeddings loaded")
    print(f"   ✅ Cross-agent memory sharing: {len(context)} context items")
    print(f"   ✅ Semantic search: {len(ai_results)} relevant results")
    print("   ✅ Memory analytics: Complete")

    # Cleanup test files
    try:
        os.remove("test_enhanced_memory.json")
        os.remove("test_embeddings.index")
        os.remove("test_embeddings.index.metadata.json")
        print("🧹 Cleaned up test files")
    except Exception:
        pass

    success = (
        len(ai_results) >= 2 and
        len(context) >= 1 and  # At least 1 context item is sufficient
        embeddings_count >= 6 and
        len(insights) >= 1
    )

    if success:
        print("\n🎉 SUCCESS: Enhanced memory store is working correctly!")
        print("   ✅ Embeddings generation and search")
        print("   ✅ Cross-agent memory sharing")
        print("   ✅ Semantic context retrieval")
        print("   ✅ Memory persistence")
    else:
        print("\n❌ FAILURE: Enhanced memory store tests failed")
        print(f"   AI results: {len(ai_results)}/2+")
        print(f"   Context items: {len(context)}/1+")
        print(f"   Embeddings: {embeddings_count}/6+")
        print(f"   Insights: {len(insights)}/1+")

    return success


if __name__ == "__main__":
    success = test_enhanced_memory()
    sys.exit(0 if success else 1)
