"""
Unit tests for slide_builder module
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from slide_builder import SlideBuilder
from layout_manager import LayoutManager
from data_structures import SlideContent, Slide


class TestSlideBuilder(unittest.TestCase):
    """Test cases for SlideBuilder class"""

    def setUp(self):
        """Set up test layout manager"""
        layout_mapping = {
            "Title Slide": 0,
            "Title, Content": 1,
            "Title, Picture": 2,
            "Title, Content, Picture": 3,
        }
        self.layout_manager = LayoutManager(layout_mapping)

    def test_slide_builder_title_only(self):
        """Test building a title-only slide"""
        builder = SlideBuilder(self.layout_manager)
        builder.set_title("Test Title")
        slide = builder.finalize()

        self.assertIsInstance(slide, Slide)
        self.assertEqual(slide.content.title, "Test Title")
        self.assertEqual(len(slide.content.bullet_points), 0)
        self.assertIsNone(slide.content.image_path)
        self.assertEqual(slide.layout_id, 0)

    def test_slide_builder_with_bullets(self):
        """Test building a slide with title and bullet points"""
        builder = SlideBuilder(self.layout_manager)
        builder.set_title("Test Title")
        builder.add_bullet_point("Point 1", level=0)
        builder.add_bullet_point("Point 2", level=1)
        slide = builder.finalize()

        self.assertEqual(slide.content.title, "Test Title")
        self.assertEqual(len(slide.content.bullet_points), 2)
        self.assertEqual(slide.content.bullet_points[0]['text'], "Point 1")
        self.assertEqual(slide.content.bullet_points[0]['level'], 0)
        self.assertEqual(slide.content.bullet_points[1]['text'], "Point 2")
        self.assertEqual(slide.content.bullet_points[1]['level'], 1)
        self.assertEqual(slide.layout_id, 1)

    def test_slide_builder_with_image(self):
        """Test building a slide with title and image"""
        builder = SlideBuilder(self.layout_manager)
        builder.set_title("Test Title")
        builder.set_image("images/test.png")
        slide = builder.finalize()

        self.assertEqual(slide.content.title, "Test Title")
        self.assertEqual(slide.content.image_path, "images/test.png")
        self.assertEqual(slide.layout_id, 2)

    def test_slide_builder_complete(self):
        """Test building a complete slide with all content types"""
        builder = SlideBuilder(self.layout_manager)
        builder.set_title("Complete Slide")
        builder.add_bullet_point("Point 1", level=0)
        builder.add_bullet_point("Subpoint", level=1)
        builder.set_image("images/test.png")
        slide = builder.finalize()

        self.assertEqual(slide.content.title, "Complete Slide")
        self.assertEqual(len(slide.content.bullet_points), 2)
        self.assertEqual(slide.content.image_path, "images/test.png")
        self.assertEqual(slide.layout_id, 3)

    def test_slide_builder_multiple_slides(self):
        """Test building multiple slides with same manager"""
        # First slide
        builder1 = SlideBuilder(self.layout_manager)
        builder1.set_title("Slide 1")
        slide1 = builder1.finalize()

        # Second slide
        builder2 = SlideBuilder(self.layout_manager)
        builder2.set_title("Slide 2")
        builder2.add_bullet_point("Content", level=0)
        slide2 = builder2.finalize()

        self.assertEqual(slide1.content.title, "Slide 1")
        self.assertEqual(slide2.content.title, "Slide 2")
        self.assertNotEqual(slide1.layout_id, slide2.layout_id)


if __name__ == '__main__':
    unittest.main()

