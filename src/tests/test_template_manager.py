"""
Unit tests for template_manager module
"""
import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from template_manager import load_template, get_layout_mapping, print_layouts


class TestTemplateManager(unittest.TestCase):
    """Test cases for template_manager module"""

    @patch('template_manager.Presentation')
    def test_load_template(self, mock_presentation_class):
        """Test loading a template"""
        mock_prs = Mock()
        mock_presentation_class.return_value = mock_prs

        template_path = "templates/test.pptx"
        result = load_template(template_path)

        mock_presentation_class.assert_called_once_with(template_path)
        self.assertEqual(result, mock_prs)

    def test_get_layout_mapping(self):
        """Test getting layout mapping from presentation"""
        # Create mock presentation with layouts
        mock_prs = Mock()
        mock_layout1 = Mock()
        mock_layout1.name = "Title Slide"
        mock_layout2 = Mock()
        mock_layout2.name = "Title, Content"
        mock_layout3 = Mock()
        mock_layout3.name = "Title, Picture"

        mock_prs.slide_layouts = [mock_layout1, mock_layout2, mock_layout3]

        mapping = get_layout_mapping(mock_prs)

        self.assertEqual(mapping["Title Slide"], 0)
        self.assertEqual(mapping["Title, Content"], 1)
        self.assertEqual(mapping["Title, Picture"], 2)
        self.assertEqual(len(mapping), 3)

    def test_get_layout_mapping_empty(self):
        """Test getting layout mapping from presentation with no layouts"""
        mock_prs = Mock()
        mock_prs.slide_layouts = []

        mapping = get_layout_mapping(mock_prs)

        self.assertEqual(len(mapping), 0)

    @patch('builtins.print')
    def test_print_layouts(self, mock_print):
        """Test printing layouts"""
        mock_prs = Mock()
        mock_layout1 = Mock()
        mock_layout1.name = "Title Slide"
        mock_layout2 = Mock()
        mock_layout2.name = "Content"

        mock_prs.slide_layouts = [mock_layout1, mock_layout2]

        print_layouts(mock_prs)

        self.assertEqual(mock_print.call_count, 2)
        mock_print.assert_any_call("Layout 0: Title Slide")
        mock_print.assert_any_call("Layout 1: Content")


if __name__ == '__main__':
    unittest.main()

