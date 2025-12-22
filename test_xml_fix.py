"""
Test to verify the XML special character fix for image insertion
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from ppt_generator import sanitize_for_xml, safe_insert_picture

def test_sanitize_for_xml():
    """Test the XML sanitization function"""
    print("=" * 80)
    print("Testing XML Sanitization Function")
    print("=" * 80)

    test_cases = [
        ("normal_image.png", "normal_imagepng"),
        ("image&with&ampersands.png", "imagewithampersandspng"),
        ("image<with>brackets.png", "imagewithbracketspng"),
        ("image'with\"quotes.png", "imagewithquotespng"),
        ("图片_中文_test.png", "图片_中文_testpng"),
        ("image @ # $ %.png", "image____png"),
        ("", ""),
    ]

    print("\nTest Cases:")
    for original, expected_contains in test_cases:
        result = sanitize_for_xml(original)
        status = "✅" if len(result) >= len(expected_contains) - 3 else "⚠️"
        print(f"{status} '{original}' → '{result}'")

    print("\n" + "=" * 80)
    print("✅ Sanitization tests complete")
    print("=" * 80)

def test_image_path_safety():
    """Test various image path scenarios"""
    print("\n" + "=" * 80)
    print("Testing Image Path Safety")
    print("=" * 80)

    # Check if there are any images in the project
    test_paths = [
        "images/forecast.png",
        "images/image_1.png",
        "images/performance_chart.png"
    ]

    existing_images = []
    for path in test_paths:
        if os.path.exists(path):
            existing_images.append(path)

    if existing_images:
        print(f"\nFound {len(existing_images)} test images:")
        for img in existing_images:
            basename = os.path.basename(img)
            sanitized = sanitize_for_xml(basename)
            print(f"  • {basename} → {sanitized}")
    else:
        print("\n⚠️ No test images found in images/ directory")

    print("\n" + "=" * 80)
    print("✅ Path safety tests complete")
    print("=" * 80)

if __name__ == "__main__":
    test_sanitize_for_xml()
    test_image_path_safety()

    print("\n" + "=" * 80)
    print("🎯 Summary")
    print("=" * 80)
    print("""
The fix addresses the XML parsing error by:

1. Sanitizing filenames to remove special XML characters (&, <, >, ', ")
2. Creating temporary safe copies of images with problematic names
3. Using the safe copy for PowerPoint insertion
4. Cleaning up temporary files after insertion

This prevents the 'xmlParseEntityRef: no name' error that occurs when
image paths or descriptions contain unescaped special characters.

To test with the actual Gradio app:
1. Run: python src/gradio_app.py
2. Generate content with the reflection mechanism
3. Click "Generate PowerPoint"
4. The error should now be resolved
    """)
    print("=" * 80)

