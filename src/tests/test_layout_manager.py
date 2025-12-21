"""
Unit tests for layout_manager module
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from layout_manager import (
    calculate_layout_encoding,
    calculate_content_encoding,
    LayoutStrategy,
    LayoutManager
)
from data_structures import SlideContent


class TestCalculateLayoutEncoding(unittest.TestCase):
    """Test cases for calculate_layout_encoding function"""

    def test_title_layout(self):
        """Test encoding for title-only layout"""
        encoding = calculate_layout_encoding("Title")
        self.assertEqual(encoding, 1)

    def test_content_layout(self):
        """Test encoding for content layout"""
        encoding = calculate_layout_encoding("Title, Content")
        self.assertEqual(encoding, 3)

    def test_picture_layout(self):
        """Test encoding for picture layout"""
        encoding = calculate_layout_encoding("Title, Picture")
        self.assertEqual(encoding, 5)

    def test_full_layout(self):
        """Test encoding for title + content + picture layout"""
        encoding = calculate_layout_encoding("Title, Content, Picture")
        self.assertEqual(encoding, 7)


class TestCalculateContentEncoding(unittest.TestCase):
    """Test cases for calculate_content_encoding function"""

    def test_title_only(self):
        """Test encoding for title-only content"""
        content = SlideContent(title="Test Title")
        encoding = calculate_content_encoding(content)
        self.assertEqual(encoding, 1)

    def test_title_with_bullets(self):
        """Test encoding for title with bullet points"""
        content = SlideContent(
            title="Test Title",
            bullet_points=[{'text': 'Point 1', 'level': 0}]
        )
        encoding = calculate_content_encoding(content)
        self.assertEqual(encoding, 3)

    def test_title_with_image(self):
        """Test encoding for title with image"""
        content = SlideContent(
            title="Test Title",
            image_path="test.png"
        )
        encoding = calculate_content_encoding(content)
        self.assertEqual(encoding, 5)

    def test_title_with_bullets_and_image(self):
        """Test encoding for complete content"""
        content = SlideContent(
            title="Test Title",
            bullet_points=[{'text': 'Point 1', 'level': 0}],
            image_path="test.png"
        )
        encoding = calculate_content_encoding(content)
        self.assertEqual(encoding, 7)


class TestLayoutStrategy(unittest.TestCase):
    """Test cases for LayoutStrategy class"""

    def test_layout_strategy_single_layout(self):
        """Test LayoutStrategy with single layout"""
        layout_group = [(0, "Title Slide")]
        strategy = LayoutStrategy(layout_group)
        content = SlideContent(title="Test")

        layout_id, layout_name = strategy.get_layout(content)
        self.assertEqual(layout_id, 0)
        self.assertEqual(layout_name, "Title Slide")

    def test_layout_strategy_multiple_layouts(self):
        """Test LayoutStrategy with multiple layouts"""
        layout_group = [
            (1, "Title, Content Layout 1"),
            (2, "Title, Content Layout 2")
        ]
        strategy = LayoutStrategy(layout_group)
        content = SlideContent(
            title="Test",
            bullet_points=[{'text': 'Point 1', 'level': 0}]
        )

        layout_id, layout_name = strategy.get_layout(content)
        self.assertIn(layout_id, [1, 2])
        self.assertIn(layout_name, ["Title, Content Layout 1", "Title, Content Layout 2"])


class TestLayoutManager(unittest.TestCase):
    """Test cases for LayoutManager class"""

    def setUp(self):
        """Set up test layout mapping"""
        self.layout_mapping = {
            "Title Slide": 0,
            "Title, Content": 1,
            "Title, Picture": 2,
            "Title, Content, Picture": 3,
        }
        self.manager = LayoutManager(self.layout_mapping)

    def test_layout_manager_initialization(self):
        """Test LayoutManager initialization"""
        self.assertIsNotNone(self.manager)
        self.assertEqual(len(self.manager.strategies), 4)
        self.assertIn(1, self.manager.strategies)
        self.assertIn(3, self.manager.strategies)
        self.assertIn(5, self.manager.strategies)
        self.assertIn(7, self.manager.strategies)

    def test_assign_layout_title_only(self):
        """Test assigning layout for title-only content"""
        content = SlideContent(title="Test Title")
        layout_id, layout_name = self.manager.assign_layout(content)
        self.assertEqual(layout_id, 0)
        self.assertEqual(layout_name, "Title Slide")

    def test_assign_layout_with_content(self):
        """Test assigning layout for title with content"""
        content = SlideContent(
            title="Test Title",
            bullet_points=[{'text': 'Point 1', 'level': 0}]
        )
        layout_id, layout_name = self.manager.assign_layout(content)
        self.assertEqual(layout_id, 1)
        self.assertEqual(layout_name, "Title, Content")

    def test_assign_layout_with_picture(self):
        """Test assigning layout for title with picture"""
        content = SlideContent(
            title="Test Title",
            image_path="test.png"
        )
        layout_id, layout_name = self.manager.assign_layout(content)
        self.assertEqual(layout_id, 2)
        self.assertEqual(layout_name, "Title, Picture")

    def test_assign_layout_complete(self):
        """Test assigning layout for complete content"""
        content = SlideContent(
            title="Test Title",
            bullet_points=[{'text': 'Point 1', 'level': 0}],
            image_path="test.png"
        )
        layout_id, layout_name = self.manager.assign_layout(content)
        self.assertEqual(layout_id, 3)
        self.assertEqual(layout_name, "Title, Content, Picture")

    def test_layout_manager_str(self):
        """Test LayoutManager string representation"""
        str_repr = str(self.manager)
        self.assertIn("LayoutManager Strategies", str_repr)
        self.assertIn("Encoding", str_repr)


if __name__ == '__main__':
    unittest.main()

