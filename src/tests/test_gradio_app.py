"""
Unit tests for gradio_app module - Core functionality only
"""
import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
import uuid

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestGradioAppHelpers(unittest.TestCase):
    """Test cases for helper functions in gradio_app"""

    @patch('gradio_app.ChatBot')
    def test_get_chatbot_instance_new_session(self, mock_chatbot_class):
        """Test creating a new chatbot instance for a session"""
        from gradio_app import get_chatbot_instance, chatbot_instances

        # Clear instances
        chatbot_instances.clear()

        mock_chatbot = Mock()
        mock_chatbot_class.return_value = mock_chatbot

        session_id = "test_session_1"
        result = get_chatbot_instance(session_id)

        self.assertEqual(result, mock_chatbot)
        self.assertIn(session_id, chatbot_instances)
        mock_chatbot_class.assert_called_once()

    @patch('gradio_app.ChatBot')
    def test_get_chatbot_instance_existing_session(self, mock_chatbot_class):
        """Test retrieving existing chatbot instance"""
        from gradio_app import get_chatbot_instance, chatbot_instances

        # Clear instances
        chatbot_instances.clear()

        mock_chatbot = Mock()
        mock_chatbot_class.return_value = mock_chatbot

        session_id = "test_session_2"

        # First call creates instance
        result1 = get_chatbot_instance(session_id)

        # Reset mock to track second call
        mock_chatbot_class.reset_mock()

        # Second call should return same instance without creating new
        result2 = get_chatbot_instance(session_id)

        self.assertEqual(result1, result2)
        mock_chatbot_class.assert_not_called()

    @patch('gradio_app.ImageAdvisor')
    def test_get_image_advisor_instance_singleton(self, mock_advisor_class):
        """Test that ImageAdvisor is a singleton"""
        import gradio_app

        # Reset global instance
        gradio_app.image_advisor_instance = None

        mock_advisor = Mock()
        mock_advisor_class.return_value = mock_advisor

        # First call creates instance
        result1 = gradio_app.get_image_advisor_instance()

        # Reset mock
        mock_advisor_class.reset_mock()

        # Second call should return same instance
        result2 = gradio_app.get_image_advisor_instance()

        self.assertEqual(result1, result2)
        mock_advisor_class.assert_not_called()


class TestMarkdownProcessing(unittest.TestCase):
    """Test cases for markdown processing functions"""

    @patch('gradio_app.parse_input_text')
    @patch('gradio_app.generate_presentation')
    @patch('gradio_app.Config')
    @patch('gradio_app.load_template')
    @patch('gradio_app.get_layout_mapping')
    @patch('gradio_app.LayoutManager')
    @patch('os.chdir')
    def test_generate_ppt_from_markdown_success(
        self, mock_chdir, mock_layout_mgr_class, mock_get_layout,
        mock_load_template, mock_config_class, mock_gen_pres, mock_parse
    ):
        """Test successful PPT generation from markdown"""
        from gradio_app import generate_ppt_from_markdown

        # Setup mocks
        mock_config = Mock()
        mock_config.ppt_template = "template.pptx"
        mock_config_class.return_value = mock_config

        mock_ppt_template = Mock()
        mock_load_template.return_value = mock_ppt_template

        mock_layout_mapping = {"Title": 0}
        mock_get_layout.return_value = mock_layout_mapping

        mock_layout_manager = Mock()
        mock_layout_mgr_class.return_value = mock_layout_manager

        mock_powerpoint_data = Mock()
        mock_parse.return_value = (mock_powerpoint_data, "Test Presentation")

        # Test
        markdown_text = "# Test\n## Slide 1\n- Point"
        result_path, status = generate_ppt_from_markdown(markdown_text)

        # Verify
        self.assertIsNotNone(result_path)
        self.assertIn("✅", status)
        self.assertIn("Test Presentation", status)
        mock_parse.assert_called_once()
        mock_gen_pres.assert_called_once()

    def test_generate_ppt_from_markdown_empty_input(self):
        """Test PPT generation with empty markdown"""
        from gradio_app import generate_ppt_from_markdown

        result_path, status = generate_ppt_from_markdown("")

        self.assertIsNone(result_path)
        self.assertIn("⚠️", status)


class TestChatFunctions(unittest.TestCase):
    """Test cases for chat functions"""

    @patch('gradio_app.LANGCHAIN_AVAILABLE', True)
    @patch('gradio_app.get_chatbot_instance')
    def test_chat_with_bot_success(self, mock_get_chatbot):
        """Test successful chat interaction"""
        from gradio_app import chat_with_bot

        mock_chatbot = Mock()
        mock_chatbot.chat_with_history.return_value = "AI response"
        mock_get_chatbot.return_value = mock_chatbot

        user_input = "Create a presentation"
        chat_history = []
        session_id = "test_session"

        updated_history, response = chat_with_bot(user_input, chat_history, session_id)

        self.assertEqual(len(updated_history), 2)
        self.assertEqual(updated_history[0]["role"], "user")
        self.assertEqual(updated_history[0]["content"], user_input)
        self.assertEqual(updated_history[1]["role"], "assistant")
        self.assertEqual(updated_history[1]["content"], "AI response")
        self.assertEqual(response, "AI response")

    def test_chat_with_bot_langchain_unavailable(self):
        """Test chat when LangChain is not available"""
        # Import the module and temporarily set LANGCHAIN_AVAILABLE to False
        import gradio_app
        original_value = gradio_app.LANGCHAIN_AVAILABLE

        try:
            gradio_app.LANGCHAIN_AVAILABLE = False

            user_input = "Create a presentation"
            chat_history = []
            session_id = "test_session"

            updated_history, response = gradio_app.chat_with_bot(user_input, chat_history, session_id)

            # When LangChain is unavailable, response is empty but error is in chat_history
            self.assertEqual(response, "")
            self.assertEqual(len(updated_history), 2)
            self.assertIn("❌", updated_history[1]["content"])
            self.assertIn("LangChain", updated_history[1]["content"])
        finally:
            # Restore original value
            gradio_app.LANGCHAIN_AVAILABLE = original_value


class TestImageEnhancement(unittest.TestCase):
    """Test cases for image enhancement functions"""

    @patch('gradio_app.get_image_advisor_instance')
    def test_enhance_markdown_with_images_success(self, mock_get_advisor):
        """Test successful image enhancement"""
        from gradio_app import enhance_markdown_with_images

        mock_advisor = Mock()
        mock_advisor.generate_images.return_value = (
            "# Enhanced\n![](image.png)",
            [("prompt", "image.png")]
        )
        mock_get_advisor.return_value = mock_advisor

        markdown_text = "# Test Presentation"
        session_id = "test_session"

        enhanced_content, status = enhance_markdown_with_images(markdown_text, session_id)

        self.assertIn("![](image.png)", enhanced_content)
        self.assertIn("✅", status)
        self.assertIn("1 images", status)

    def test_enhance_markdown_with_images_empty_input(self):
        """Test image enhancement with empty markdown"""
        from gradio_app import enhance_markdown_with_images

        enhanced_content, status = enhance_markdown_with_images("", "session")

        self.assertEqual(enhanced_content, "")
        self.assertIn("⚠️", status)


if __name__ == '__main__':
    unittest.main()

