"""
Test script to verify the Gradio app functionality
"""
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")

    try:
        import gradio as gr
        print("✅ Gradio imported successfully")
    except ImportError as e:
        print(f"❌ Gradio import failed: {e}")
        return False

    try:
        from langchain_core.messages import HumanMessage, SystemMessage
        print("✅ LangChain Core imported successfully")
    except ImportError as e:
        print(f"❌ LangChain Core import failed: {e}")
        return False

    try:
        from azure_openai import chat_model
        print("✅ Azure OpenAI imported successfully")
    except Exception as e:
        print(f"⚠️  Azure OpenAI import warning: {e}")

    try:
        from input_parser import parse_input_text
        from ppt_generator import generate_presentation
        from layout_manager import LayoutManager
        from config import Config
        print("✅ ChatPPT modules imported successfully")
    except ImportError as e:
        print(f"❌ ChatPPT modules import failed: {e}")
        return False

    return True


def test_ppt_generation():
    """Test PowerPoint generation with sample markdown"""
    print("\nTesting PPT generation...")

    try:
        from input_parser import parse_input_text
        from ppt_generator import generate_presentation
        from layout_manager import LayoutManager
        from config import Config
        import datetime

        # Change to project directory
        os.chdir(os.path.dirname(__file__))

        config = Config()
        layout_manager = LayoutManager(config.layout_mapping)

        # Sample markdown
        test_markdown = """# Test Presentation

## Introduction
- This is a test slide
- Testing bullet points

## Conclusion
- Test completed
"""

        # Parse and generate
        powerpoint_data, presentation_title = parse_input_text(test_markdown, layout_manager)

        # Create output
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"output/test_presentation_{timestamp}.pptx"
        os.makedirs("output", exist_ok=True)

        generate_presentation(powerpoint_data, config.ppt_template, output_file)

        if os.path.exists(output_file):
            print(f"✅ PowerPoint generated successfully: {output_file}")
            return True
        else:
            print("❌ PowerPoint file was not created")
            return False

    except Exception as e:
        print(f"❌ PPT generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    print("=" * 60)
    print("ChatPPT Gradio App - Functionality Test")
    print("=" * 60)
    print()

    # Test imports
    if not test_imports():
        print("\n⚠️  Some imports failed. Please install missing packages:")
        print("   pip install -r requirements.txt")
        return

    # Test PPT generation
    if not test_ppt_generation():
        print("\n⚠️  PPT generation test failed")
        return

    print("\n" + "=" * 60)
    print("✅ All tests passed! You can now run the Gradio app:")
    print("   cd src")
    print("   python gradio_app.py")
    print("=" * 60)


if __name__ == "__main__":
    main()

