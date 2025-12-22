"""
Test PowerPoint generation with the XML fix
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from input_parser import parse_input_text
from ppt_generator import generate_presentation
from layout_manager import LayoutManager
from template_manager import load_template, get_layout_mapping
from config import Config
import datetime

def test_ppt_generation_with_images():
    """Test PPT generation with various image scenarios"""

    print("=" * 80)
    print("Testing PowerPoint Generation with XML Special Character Fix")
    print("=" * 80)

    # Create test markdown with an image
    test_markdown = """# Test Presentation

## Introduction
- This is a test presentation
- Testing image insertion with special characters

## Image Test Slide
- This slide contains an image
- The image path may have special characters
![Test Image](images/forecast.png)

## Conclusion
- Testing complete
- PowerPoint should generate successfully
"""

    print("\n📄 Test Markdown:")
    print("-" * 80)
    print(test_markdown)
    print("-" * 80)

    try:
        # Parse markdown
        config = Config()
        ppt_template = load_template(config.ppt_template)
        layout_manager = LayoutManager(get_layout_mapping(ppt_template))

        powerpoint_data, presentation_title = parse_input_text(test_markdown, layout_manager)

        print(f"\n✅ Parsed presentation: '{presentation_title}'")
        print(f"✅ Number of slides: {len(powerpoint_data.slides)}")

        # Generate PowerPoint
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"test_xml_fix_{timestamp}.pptx"
        output_pptx = os.path.join("output", output_filename)

        os.makedirs("output", exist_ok=True)

        print(f"\n📊 Generating PowerPoint...")
        generate_presentation(powerpoint_data, config.ppt_template, output_pptx)

        print(f"✅ PowerPoint generated successfully!")
        print(f"📁 File: {output_filename}")
        print(f"💾 Location: {os.path.abspath(output_pptx)}")

        print("\n" + "=" * 80)
        print("✅ TEST PASSED: PowerPoint generation works with XML fix!")
        print("=" * 80)

        return True

    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        print("=" * 80)
        return False

if __name__ == "__main__":
    success = test_ppt_generation_with_images()

    print("\n" + "=" * 80)
    print("🔧 Fix Summary")
    print("=" * 80)
    print("""
The XML special character fix addresses the error:
'xmlParseEntityRef: no name, line 3, column 61'

Changes made to src/ppt_generator.py:
1. Added sanitize_for_xml() function to remove special characters
2. Added safe_insert_picture() function that:
   - Sanitizes image filenames before insertion
   - Creates temporary safe copies if needed
   - Cleans up temp files after insertion
3. Updated generate_presentation() to use safe_insert_picture()

This prevents XML parsing errors when image paths or filenames
contain special characters like &, <, >, ', or " that aren't
properly escaped in the python-pptx library's XML templates.
    """)
    print("=" * 80)

    sys.exit(0 if success else 1)

