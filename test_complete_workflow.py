"""
Test the complete workflow: Reflection chatbot -> Markdown -> PowerPoint
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from reflection_chatbot import ReflectionChatBot
from input_parser import parse_input_text
from ppt_generator import generate_presentation
from layout_manager import LayoutManager
from template_manager import load_template, get_layout_mapping
from config import Config
from logger import LOG
import datetime

def test_complete_workflow():
    """Test the complete workflow from reflection to PPT generation"""

    print("=" * 80)
    print("Testing Complete Workflow: Reflection -> Markdown -> PPT")
    print("=" * 80)

    # Step 1: Generate content with reflection
    print("\n📝 Step 1: Generate content with reflection mechanism")
    print("-" * 80)

    prompt_file = os.path.join("prompts", "content_assistant.txt")
    chatbot = ReflectionChatBot(prompt_file=prompt_file, session_id="workflow_test")

    user_input = "创建一个关于Python编程的简短演讲，包含：介绍、主要特性、应用领域三个部分"

    print(f"User request: {user_input}\n")

    response, feedbacks = chatbot.chat_with_reflection(user_input, "workflow_test")

    print(f"✅ Generated markdown content ({len(response)} chars)")
    print(f"✅ Received {len(feedbacks)} rounds of feedback")

    # Display a preview of the markdown
    preview_length = 500
    print(f"\n📄 Markdown Preview (first {preview_length} chars):")
    print("-" * 80)
    print(response[:preview_length] + "..." if len(response) > preview_length else response)
    print("-" * 80)

    # Step 2: Parse markdown to PowerPoint structure
    print("\n📊 Step 2: Parse markdown to PowerPoint structure")
    print("-" * 80)

    try:
        config = Config()
        ppt_template = load_template(config.ppt_template)
        layout_manager = LayoutManager(get_layout_mapping(ppt_template))

        powerpoint_data, presentation_title = parse_input_text(response, layout_manager)

        print(f"✅ Parsed presentation: '{presentation_title}'")
        print(f"✅ Number of slides: {len(powerpoint_data)}")

        # Step 3: Generate PowerPoint file
        print("\n💼 Step 3: Generate PowerPoint file")
        print("-" * 80)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        clean_title = "Python_Presentation"
        output_filename = f"{clean_title}_{timestamp}.pptx"
        output_pptx = os.path.join("output", output_filename)

        os.makedirs("output", exist_ok=True)

        generate_presentation(powerpoint_data, config.ppt_template, output_pptx)

        print(f"✅ PowerPoint generated successfully!")
        print(f"📁 File: {output_filename}")
        print(f"💾 Location: {os.path.abspath(output_pptx)}")

        # Step 4: Display feedback summary
        print("\n🔄 Step 4: Reflection Feedback Summary")
        print("=" * 80)

        for i, feedback in enumerate(feedbacks, 1):
            preview = feedback[:200] + "..." if len(feedback) > 200 else feedback
            print(f"\nRound {i} Feedback (preview):")
            print(preview)

        print("\n" + "=" * 80)
        print("✅ COMPLETE WORKFLOW TEST SUCCESSFUL!")
        print("=" * 80)
        print("\nSummary:")
        print(f"  - Generated {len(response)} characters of markdown content")
        print(f"  - Completed {len(feedbacks)} rounds of AI reflection")
        print(f"  - Created {len(powerpoint_data)} slides")
        print(f"  - Saved PowerPoint to: {output_filename}")
        print("=" * 80)

    except Exception as e:
        print(f"\n❌ Error during workflow: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

    return True

if __name__ == "__main__":
    success = test_complete_workflow()
    sys.exit(0 if success else 1)

