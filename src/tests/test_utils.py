"""
Unit tests for utils module
"""
import unittest
import sys
import os
from unittest.mock import Mock, MagicMock

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils import remove_all_slides


class TestUtils(unittest.TestCase):
    """Test cases for utils module"""

    def test_remove_all_slides(self):
        """Test removing all slides from presentation"""
        # Create mock presentation
        mock_prs = Mock()
        mock_slides = Mock()
        mock_sld_id_lst = Mock()

        # Create mock slide elements
        mock_slide1 = Mock()
        mock_slide2 = Mock()
        mock_slide3 = Mock()

        # Setup the mock structure
        mock_sld_id_lst.__iter__ = Mock(return_value=iter([mock_slide1, mock_slide2, mock_slide3]))
        mock_slides._sldIdLst = mock_sld_id_lst
        mock_prs.slides = mock_slides

        # Call the function
        remove_all_slides(mock_prs)

        # Verify remove was called for each slide
        self.assertEqual(mock_sld_id_lst.remove.call_count, 3)
        mock_sld_id_lst.remove.assert_any_call(mock_slide1)
        mock_sld_id_lst.remove.assert_any_call(mock_slide2)
        mock_sld_id_lst.remove.assert_any_call(mock_slide3)

    def test_remove_all_slides_empty_presentation(self):
        """Test removing slides from empty presentation"""
        # Create mock presentation with no slides
        mock_prs = Mock()
        mock_slides = Mock()
        mock_sld_id_lst = Mock()

        mock_sld_id_lst.__iter__ = Mock(return_value=iter([]))
        mock_slides._sldIdLst = mock_sld_id_lst
        mock_prs.slides = mock_slides

        # Call the function
        remove_all_slides(mock_prs)

        # Verify remove was not called
        mock_sld_id_lst.remove.assert_not_called()


if __name__ == '__main__':
    unittest.main()

