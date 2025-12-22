"""
Simple debug test for reflection chatbot
"""
import sys
import os
import asyncio

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from reflection_chatbot import ReflectionChatBot
from logger import LOG

async def test_async():
    """Test the reflection chatbot async"""

    print("=" * 80)
    print("Testing Reflection ChatBot - ASYNC DEBUG")
    print("=" * 80)

    # Create the chatbot instance
    prompt_file = os.path.join("prompts", "content_assistant.txt")
    chatbot = ReflectionChatBot(prompt_file=prompt_file, session_id="debug_test")

    # Simple test prompt
    user_input = "Create a simple 3-slide presentation about Python programming: Introduction, Features, and Conclusion"

    print(f"\n📝 User Input:\n{user_input}\n")
    print("🔄 Starting async reflection process...\n")

    # Generate with reflection
    response, feedbacks = await chatbot.generate_with_reflection(user_input, "debug_test")

    print("=" * 80)
    print("✅ Final Generated Content:")
    print("=" * 80)
    print(response[:500] + "..." if len(response) > 500 else response)
    print("\n")

    print("=" * 80)
    print(f"🔄 Reflection Feedback ({len(feedbacks)} rounds):")
    print("=" * 80)
    for i, feedback in enumerate(feedbacks, 1):
        print(f"\n--- Round {i} Feedback ---")
        print(feedback[:300] + "..." if len(feedback) > 300 else feedback)
        print()

    print("=" * 80)
    print(f"✅ Test completed! Got {len(feedbacks)} feedback rounds")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_async())

