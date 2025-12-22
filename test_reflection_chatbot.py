"""
Test script for the reflection chatbot
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from reflection_chatbot import ReflectionChatBot
from logger import LOG

def test_reflection_chatbot():
    """Test the reflection chatbot with a simple prompt"""

    print("=" * 80)
    print("Testing Reflection ChatBot")
    print("=" * 80)

    # Create the chatbot instance
    prompt_file = os.path.join("prompts", "content_assistant.txt")
    chatbot = ReflectionChatBot(prompt_file=prompt_file, session_id="test_session")

    # Test prompt
    user_input = "我想做一个关于人工智能的演讲，包含人工智能的定义、应用领域和未来展望三个部分"

    print(f"\n📝 User Input:\n{user_input}\n")
    print("🔄 Starting reflection process...\n")

    # Generate with reflection
    response, feedbacks = chatbot.chat_with_reflection(user_input, "test_session")

    print("=" * 80)
    print("✅ Final Generated Content:")
    print("=" * 80)
    print(response)
    print("\n")

    print("=" * 80)
    print(f"🔄 Reflection Feedback ({len(feedbacks)} rounds):")
    print("=" * 80)
    for i, feedback in enumerate(feedbacks, 1):
        print(f"\n--- Round {i} Feedback ---")
        print(feedback)
        print()

    print("=" * 80)
    print("✅ Test completed successfully!")
    print("=" * 80)

if __name__ == "__main__":
    test_reflection_chatbot()

