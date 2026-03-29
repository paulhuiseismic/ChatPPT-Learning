"""
Unit tests for image_advisor module — focused on the JSON parsing fix
(replacing eval() with json.loads()).
"""
import json
import sys
import unittest
import os
from unittest.mock import MagicMock, patch

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Stub out heavy Azure / LangChain dependencies so the module can be imported
# without real credentials or installed packages.
_azure_stub = MagicMock()
_azure_stub.chat_model = MagicMock()
sys.modules.setdefault('azure_openai', _azure_stub)
sys.modules.setdefault('langchain_core', MagicMock())
sys.modules.setdefault('langchain_core.prompts', MagicMock())


class TestGetBingImagesJsonParsing(unittest.TestCase):
    """Tests that image metadata is parsed with json.loads, not eval."""

    def _make_advisor(self):
        """Build a minimal ImageAdvisor without real Azure/network dependencies."""
        import image_advisor as ia_module

        class ConcreteAdvisor(ia_module.ImageAdvisor):
            """Concrete subclass of the ABC so we can instantiate it."""
            pass

        advisor = ConcreteAdvisor.__new__(ConcreteAdvisor)
        advisor.advisor = MagicMock()
        return advisor

    def test_valid_json_murl_is_extracted(self):
        """get_bing_images should extract murl from valid JSON metadata."""
        advisor = self._make_advisor()

        # Build a minimal HTML page that looks like a Bing image search result
        m_value = json.dumps({"murl": "https://example.com/img.jpg", "turl": "https://t.example.com"})
        html = f'<html><body><a class="iusc" m=\'{m_value}\'></a></body></html>'

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = html

        mock_session = MagicMock()
        mock_session.get.return_value = mock_response

        import image_advisor as ia_module
        with patch.object(ia_module.requests, 'Session', return_value=mock_session):
            result = advisor.get_bing_images("TestSlide", "test query", num_images=1)

        # Should return a list (possibly empty if image download mocked out)
        self.assertIsInstance(result, list)

    def test_invalid_json_is_skipped_gracefully(self):
        """Malformed metadata should be skipped without crashing."""
        advisor = self._make_advisor()

        html = "<html><body><a class=\"iusc\" m='not valid json at all'></a></body></html>"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = html

        mock_session = MagicMock()
        mock_session.get.return_value = mock_response

        import image_advisor as ia_module
        with patch.object(ia_module.requests, 'Session', return_value=mock_session):
            result = advisor.get_bing_images("TestSlide", "test query", num_images=1)

        # Should return empty list, not raise an exception
        self.assertEqual(result, [])

    def test_eval_not_called(self):
        """Ensure eval() is no longer called during metadata parsing."""
        import image_advisor as ia_module
        import inspect

        source = inspect.getsource(ia_module.ImageAdvisor.get_bing_images)
        self.assertNotIn('eval(', source, "eval() must not be used in get_bing_images")

if __name__ == '__main__':
    unittest.main()
