"""
Test script for the enhanced Gradio app with ChatBot and ImageAdvisor
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test all necessary imports"""
    print("Testing imports...")

    try:
        from chatbot import ChatBot
        print("✅ ChatBot imported successfully")
    except Exception as e:
        print(f"❌ Failed to import ChatBot: {e}")
        return False

    try:
        from image_advisor import ImageAdvisor
        print("✅ ImageAdvisor imported successfully")
    except Exception as e:
        print(f"❌ Failed to import ImageAdvisor: {e}")
        return False

    try:
        from gradio_app import create_gradio_interface
        print("✅ Gradio app imported successfully")
    except Exception as e:
        print(f"❌ Failed to import Gradio app: {e}")
        return False

    return True


def test_chatbot():
    """Test ChatBot functionality"""
    print("\nTesting ChatBot...")

    try:
        from chatbot import ChatBot

        # Create chatbot instance
        chatbot = ChatBot(
            prompt_file="./prompts/content_formatter.txt",
            session_id="test_session"
        )
        print("✅ ChatBot instance created")

        # Test chat
        response = chatbot.chat_with_history("测试消息", "test_session")
        print(f"✅ ChatBot responded: {response[:100]}...")

        return True
    except Exception as e:
        print(f"❌ ChatBot test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_image_advisor():
    """Test ImageAdvisor functionality"""
    print("\nTesting ImageAdvisor...")

    try:
        from image_advisor import ImageAdvisor

        # Create advisor instance
        advisor = ImageAdvisor(prompt_file="./prompts/image_advisor.txt")
        print("✅ ImageAdvisor instance created")

        # Test keyword extraction
        test_advice = "[Slide 1]: AI technology\n[Slide 2]: Machine learning"
        keywords = advisor.get_keywords(test_advice)
        print(f"✅ Keyword extraction works: {keywords}")

        return True
    except Exception as e:
        print(f"❌ ImageAdvisor test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_gradio_interface():
    """Test Gradio interface creation"""
    print("\nTesting Gradio interface...")

    try:
        from gradio_app import create_gradio_interface

        demo = create_gradio_interface()
        print("✅ Gradio interface created successfully")
        print(f"   Demo type: {type(demo)}")

        return True
    except Exception as e:
        print(f"❌ Gradio interface test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("Enhanced ChatPPT Gradio App - Test Suite")
    print("=" * 60)

    results = []

    # Test imports
    results.append(("Imports", test_imports()))

    # Test ChatBot
    results.append(("ChatBot", test_chatbot()))

    # Test ImageAdvisor
    results.append(("ImageAdvisor", test_image_advisor()))

    # Test Gradio Interface
    results.append(("Gradio Interface", test_gradio_interface()))

    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:20s}: {status}")

    all_passed = all(result for _, result in results)

    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! The app is ready to use.")
        print("\nTo start the app, run:")
        print("  python src/gradio_app.py")
        print("\nOr use the batch file:")
        print("  run_gradio.bat")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    print("=" * 60)

    return all_passed


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

