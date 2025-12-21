"""
Unit tests for input_parser module
"""
import unittest
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from input_parser import parse_input_text, parse_bullet_point_level
from layout_manager import LayoutManager
from data_structures import PowerPoint


class TestParseBulletPointLevel(unittest.TestCase):
    """Test cases for parse_bullet_point_level function"""

    def test_no_indent(self):
        """Test parsing bullet point with no indentation"""
        level, text = parse_bullet_point_level("- First level")
        self.assertEqual(level, 0)
        self.assertEqual(text, "First level")

    def test_single_indent(self):
        """Test parsing bullet point with single indentation"""
        level, text = parse_bullet_point_level("  - Second level")
        self.assertEqual(level, 1)
        self.assertEqual(text, "Second level")

    def test_double_indent(self):
        """Test parsing bullet point with double indentation"""
        level, text = parse_bullet_point_level("    - Third level")
        self.assertEqual(level, 2)
        self.assertEqual(text, "Third level")


class TestParseInputText(unittest.TestCase):
    """Test cases for parse_input_text function"""

    def setUp(self):
        """Set up test layout manager"""
        layout_mapping = {
            "Title Slide": 0,
            "Title, Content": 1,
            "Title, Picture": 2,
            "Title, Content, Picture": 3,
        }
        self.layout_manager = LayoutManager(layout_mapping)

    def test_parse_title_only(self):
        """Test parsing presentation with title only"""
        markdown = "# Test Presentation"
        ppt, title = parse_input_text(markdown, self.layout_manager)

        self.assertEqual(title, "Test Presentation")
        self.assertEqual(ppt.title, "Test Presentation")
        self.assertEqual(len(ppt.slides), 1)
        self.assertEqual(ppt.slides[0].content.title, "Test Presentation")

    def test_parse_with_single_slide(self):
        """Test parsing presentation with title and one content slide"""
        markdown = """# Test Presentation
## First Slide
- Bullet point 1
- Bullet point 2"""

        ppt, title = parse_input_text(markdown, self.layout_manager)

        self.assertEqual(title, "Test Presentation")
        self.assertEqual(len(ppt.slides), 2)
        self.assertEqual(ppt.slides[0].content.title, "Test Presentation")
        self.assertEqual(ppt.slides[1].content.title, "First Slide")
        self.assertEqual(len(ppt.slides[1].content.bullet_points), 2)

    def test_parse_with_multiple_slides(self):
        """Test parsing presentation with multiple slides"""
        markdown = """# Test Presentation
## Slide 1
- Point 1

## Slide 2
- Point A
- Point B"""

        ppt, title = parse_input_text(markdown, self.layout_manager)

        self.assertEqual(len(ppt.slides), 3)  # Title + 2 content slides
        self.assertEqual(ppt.slides[1].content.title, "Slide 1")
        self.assertEqual(ppt.slides[2].content.title, "Slide 2")

    def test_parse_with_nested_bullets(self):
        """Test parsing presentation with nested bullet points"""
        markdown = """# Test Presentation
## Content Slide
- Level 0 point
  - Level 1 point
    - Level 2 point"""

        ppt, title = parse_input_text(markdown, self.layout_manager)

        content_slide = ppt.slides[1]
        self.assertEqual(len(content_slide.content.bullet_points), 3)
        self.assertEqual(content_slide.content.bullet_points[0]['level'], 0)
        self.assertEqual(content_slide.content.bullet_points[1]['level'], 1)
        self.assertEqual(content_slide.content.bullet_points[2]['level'], 2)

    def test_parse_with_image(self):
        """Test parsing presentation with image"""
        markdown = """# Test Presentation
## Slide with Image
- Content point
![alt text](images/test.png)"""

        ppt, title = parse_input_text(markdown, self.layout_manager)

        image_slide = ppt.slides[1]
        self.assertEqual(image_slide.content.image_path, "images/test.png")
        self.assertEqual(len(image_slide.content.bullet_points), 1)

    def test_parse_empty_lines(self):
        """Test parsing presentation with empty lines"""
        markdown = """# Test Presentation

## Slide 1

- Point 1

- Point 2"""

        ppt, title = parse_input_text(markdown, self.layout_manager)

        self.assertEqual(len(ppt.slides), 2)
        self.assertEqual(len(ppt.slides[1].content.bullet_points), 2)

    def test_parse_complex_presentation(self):
        """Test parsing a complex presentation"""
        markdown = """# AI Technology Overview

## Introduction to AI
- What is AI?
  - Machine Learning
  - Deep Learning
- Applications

## Machine Learning
- Supervised Learning
- Unsupervised Learning
![ml diagram](images/ml.png)

## Conclusion
- Summary points"""

        ppt, title = parse_input_text(markdown, self.layout_manager)

        self.assertEqual(title, "AI Technology Overview")
        self.assertEqual(len(ppt.slides), 4)  # Title + 3 content slides

        # Check Introduction slide
        intro_slide = ppt.slides[1]
        self.assertEqual(intro_slide.content.title, "Introduction to AI")
        self.assertEqual(len(intro_slide.content.bullet_points), 4)

        # Check Machine Learning slide has image
        ml_slide = ppt.slides[2]
        self.assertEqual(ml_slide.content.title, "Machine Learning")
        self.assertEqual(ml_slide.content.image_path, "images/ml.png")


if __name__ == '__main__':
    unittest.main()

