"""
Unit tests for chat_history module
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from chat_history import get_session_history, store
    from langchain_core.chat_history import InMemoryChatMessageHistory
    from langchain_core.messages import HumanMessage, AIMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False


@unittest.skipUnless(LANGCHAIN_AVAILABLE, "langchain-core not available")
class TestChatHistory(unittest.TestCase):
    """Test cases for chat_history module"""

    def setUp(self):
        """Clear the store before each test"""
        store.clear()

    def test_get_session_history_new_session(self):
        """Test getting history for a new session"""
        session_id = "test_session_1"
        history = get_session_history(session_id)

        self.assertIsInstance(history, InMemoryChatMessageHistory)
        self.assertEqual(len(history.messages), 0)

    def test_get_session_history_existing_session(self):
        """Test getting history for an existing session"""
        session_id = "test_session_2"

        # First call creates the session
        history1 = get_session_history(session_id)
        history1.add_message(HumanMessage(content="Hello"))

        # Second call should return the same session with history
        history2 = get_session_history(session_id)

        self.assertEqual(len(history2.messages), 1)
        self.assertEqual(history2.messages[0].content, "Hello")

    def test_multiple_sessions(self):
        """Test managing multiple independent sessions"""
        session1 = "session_1"
        session2 = "session_2"

        history1 = get_session_history(session1)
        history1.add_message(HumanMessage(content="Message in session 1"))

        history2 = get_session_history(session2)
        history2.add_message(HumanMessage(content="Message in session 2"))

        # Verify sessions are independent
        self.assertEqual(len(history1.messages), 1)
        self.assertEqual(len(history2.messages), 1)
        self.assertEqual(history1.messages[0].content, "Message in session 1")
        self.assertEqual(history2.messages[0].content, "Message in session 2")

    def test_session_persistence(self):
        """Test that session history persists across multiple calls"""
        session_id = "persistent_session"

        # Add messages in multiple calls
        history1 = get_session_history(session_id)
        history1.add_message(HumanMessage(content="First message"))

        history2 = get_session_history(session_id)
        history2.add_message(AIMessage(content="Response"))

        history3 = get_session_history(session_id)

        # All messages should be present
        self.assertEqual(len(history3.messages), 2)
        self.assertEqual(history3.messages[0].content, "First message")
        self.assertEqual(history3.messages[1].content, "Response")


if __name__ == '__main__':
    unittest.main()

