"""
Unit tests for data_structures module
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_structures import SlideContent, Slide, PowerPoint


class TestSlideContent(unittest.TestCase):
    """Test cases for SlideContent dataclass"""

    def test_slide_content_creation_with_defaults(self):
        """Test creating SlideContent with default values"""
        content = SlideContent(title="Test Title")
        self.assertEqual(content.title, "Test Title")
        self.assertEqual(content.bullet_points, [])
        self.assertIsNone(content.image_path)

    def test_slide_content_with_all_fields(self):
        """Test creating SlideContent with all fields"""
        bullet_points = [
            {'text': 'Point 1', 'level': 0},
            {'text': 'Point 2', 'level': 1}
        ]
        content = SlideContent(
            title="Complete Title",
            bullet_points=bullet_points,
            image_path="images/test.png"
        )
        self.assertEqual(content.title, "Complete Title")
        self.assertEqual(len(content.bullet_points), 2)
        self.assertEqual(content.image_path, "images/test.png")


class TestSlide(unittest.TestCase):
    """Test cases for Slide dataclass"""

    def test_slide_creation(self):
        """Test creating a Slide"""
        content = SlideContent(title="Slide Title")
        slide = Slide(
            layout_id=1,
            layout_name="Title Slide",
            content=content
        )
        self.assertEqual(slide.layout_id, 1)
        self.assertEqual(slide.layout_name, "Title Slide")
        self.assertEqual(slide.content.title, "Slide Title")


class TestPowerPoint(unittest.TestCase):
    """Test cases for PowerPoint dataclass"""

    def test_powerpoint_creation_empty(self):
        """Test creating empty PowerPoint"""
        ppt = PowerPoint(title="Test Presentation")
        self.assertEqual(ppt.title, "Test Presentation")
        self.assertEqual(ppt.slides, [])

    def test_powerpoint_with_slides(self):
        """Test creating PowerPoint with slides"""
        content1 = SlideContent(title="Slide 1")
        slide1 = Slide(layout_id=0, layout_name="Title", content=content1)

        content2 = SlideContent(
            title="Slide 2",
            bullet_points=[{'text': 'Point 1', 'level': 0}]
        )
        slide2 = Slide(layout_id=1, layout_name="Content", content=content2)

        ppt = PowerPoint(title="Test Presentation", slides=[slide1, slide2])
        self.assertEqual(len(ppt.slides), 2)
        self.assertEqual(ppt.slides[0].content.title, "Slide 1")
        self.assertEqual(ppt.slides[1].content.title, "Slide 2")

    def test_powerpoint_str_representation(self):
        """Test PowerPoint string representation"""
        content = SlideContent(
            title="Test Slide",
            bullet_points=[{'text': 'Bullet 1', 'level': 0}]
        )
        slide = Slide(layout_id=1, layout_name="Content", content=content)
        ppt = PowerPoint(title="Test", slides=[slide])

        str_repr = str(ppt)
        self.assertIn("Test", str_repr)
        self.assertIn("Test Slide", str_repr)
        self.assertIn("Content", str_repr)


if __name__ == '__main__':
    unittest.main()

