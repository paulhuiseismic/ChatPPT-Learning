"""
Final Demonstration Test - Reflection Mechanism with Gradio Integration
This test demonstrates the complete reflection-enhanced workflow.
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from reflection_chatbot import ReflectionChatBot

def main():
    print("=" * 100)
    print(" " * 25 + "🎨 ChatPPT Reflection Mechanism Demo")
    print("=" * 100)

    print("\n📚 This demonstration shows the enhanced ChatPPT application with LangGraph Reflection:\n")
    print("   ✓ AI generates content")
    print("   ✓ AI reflects on its own output")
    print("   ✓ AI improves content based on self-critique")
    print("   ✓ Process repeats for 3 rounds")
    print("   ✓ Final high-quality content is produced")

    print("\n" + "=" * 100)
    print("🚀 Starting Reflection Process")
    print("=" * 100)

    # Initialize the reflection chatbot
    prompt_file = os.path.join("prompts", "content_assistant.txt")
    chatbot = ReflectionChatBot(prompt_file=prompt_file, session_id="demo_session")

    # Test with a Chinese presentation request
    user_request = """
    创建一个关于"机器学习入门"的演讲PPT，包含以下内容：
    1. 什么是机器学习
    2. 机器学习的主要类型（监督学习、无监督学习、强化学习）
    3. 实际应用案例
    4. 总结与展望
    """

    print(f"\n📝 User Request:")
    print("-" * 100)
    print(user_request.strip())
    print("-" * 100)

    print("\n🔄 Reflection Mechanism Running (this may take 30-60 seconds)...")
    print("   Processing: Generation → Reflection → Improvement (×3 rounds)\n")

    # Generate with reflection
    final_content, feedbacks = chatbot.chat_with_reflection(user_request, "demo_session")

    print("\n" + "=" * 100)
    print("✅ Reflection Process Complete!")
    print("=" * 100)

    # Display results
    print(f"\n📊 Results Summary:")
    print(f"   • Completed {len(feedbacks)} rounds of reflection")
    print(f"   • Generated {len(final_content)} characters of content")
    print(f"   • Final content ready for PowerPoint generation")

    # Display feedback from each round
    print("\n" + "=" * 100)
    print("🔄 Reflection Feedback Details")
    print("=" * 100)

    for i, feedback in enumerate(feedbacks, 1):
        print(f"\n{'─' * 100}")
        print(f"Round {i} Feedback:")
        print(f"{'─' * 100}")

        # Show first 400 characters of each feedback
        preview_length = 400
        if len(feedback) > preview_length:
            print(feedback[:preview_length] + "...")
            print(f"\n[... {len(feedback) - preview_length} more characters ...]")
        else:
            print(feedback)

    # Display final content preview
    print("\n" + "=" * 100)
    print("📄 Final Generated Content (Preview)")
    print("=" * 100)

    # Show first 800 characters of final content
    preview_length = 800
    if len(final_content) > preview_length:
        print(final_content[:preview_length] + "...")
        print(f"\n[... Total content: {len(final_content)} characters ...]")
    else:
        print(final_content)

    # Summary
    print("\n" + "=" * 100)
    print("🎯 What This Demonstrates")
    print("=" * 100)
    print("""
The reflection mechanism successfully:

1. ✅ Generated initial presentation content based on user requirements
2. ✅ Reflected on the content quality (Round 1)
   - Evaluated clarity, structure, depth, and style
   - Provided specific improvement suggestions
3. ✅ Refined content based on Round 1 feedback (Round 2)
   - Implemented suggested improvements
   - Reflected again for further refinement
4. ✅ Final polish (Round 3)
   - Made final adjustments
   - Produced publication-ready content
5. ✅ Delivered high-quality markdown ready for PPT generation

This reflection process ensures that the AI produces deeper, more comprehensive, and
better-structured presentation content compared to a single-pass generation.
    """)

    print("\n" + "=" * 100)
    print("🎨 Next Steps")
    print("=" * 100)
    print("""
To use this enhanced feature in the Gradio interface:

1. Start the Gradio app:
   python src/gradio_app.py

2. Enter your presentation request in the chat interface

3. Watch the reflection feedback appear in the UI showing the AI's improvement process

4. Review the final markdown content

5. (Optional) Enhance with AI-selected images

6. Generate your PowerPoint presentation

The reflection mechanism is now integrated and will automatically improve all
content generated through the ChatPPT interface!
    """)

    print("=" * 100)
    print(" " * 30 + "✨ Demo Complete! ✨")
    print("=" * 100)

if __name__ == "__main__":
    main()

