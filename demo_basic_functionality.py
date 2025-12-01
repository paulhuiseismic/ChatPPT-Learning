"""
Demo script to test basic ChatPPT functionality without Gradio
This script demonstrates the core features:
1. Reading markdown input
2. Parsing it to PowerPoint data structure
3. Generating PowerPoint presentation
"""
import os
import sys
import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from input_parser import parse_input_text
from ppt_generator import generate_presentation
from layout_manager import LayoutManager
from config import Config
from logger import LOG


def demo_markdown_to_ppt():
    """Demonstrate converting markdown to PowerPoint"""
    print("=" * 70)
    print("ChatPPT Basic Functionality Demo")
    print("=" * 70)
    print()

    # Sample markdown content
    sample_markdown = """# AI Technology Overview

## Introduction to AI
- Artificial Intelligence is transforming industries
- Machine Learning and Deep Learning are key technologies
- Applications are growing exponentially

## Key Applications
- Healthcare: Disease diagnosis and drug discovery
- Finance: Fraud detection and algorithmic trading
- Transportation: Autonomous vehicles
![AI Growth](images/forecast.png)

## Future Trends
- More powerful AI models
- Ethical AI development
- AI democratization

## Conclusion
- AI is the future
- Continuous learning is essential
"""

    print("Sample Markdown Input:")
    print("-" * 70)
    print(sample_markdown)
    print("-" * 70)
    print()

    try:
        # Change to project directory
        os.chdir(os.path.dirname(__file__))

        # Load configuration
        config = Config()
        layout_manager = LayoutManager(config.layout_mapping)

        print("✅ Configuration loaded successfully")
        print(f"   Template: {config.ppt_template}")
        print()

        # Parse markdown
        powerpoint_data, presentation_title = parse_input_text(sample_markdown, layout_manager)

        print("✅ Markdown parsed successfully")
        print(f"   Title: {presentation_title}")
        print(f"   Number of slides: {len(powerpoint_data.slides)}")
        print()

        # Display slide information
        print("Slide Structure:")
        for i, slide in enumerate(powerpoint_data.slides, 1):
            print(f"   Slide {i}: {slide.content.title}")
            if slide.content.bullet_points:
                print(f"     - {len(slide.content.bullet_points)} bullet points")
            if slide.content.image_path:
                print(f"     - Image: {slide.content.image_path}")
        print()

        # Generate PowerPoint
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"demo_presentation_{timestamp}.pptx"
        output_path = os.path.join("output", output_filename)

        os.makedirs("output", exist_ok=True)

        generate_presentation(powerpoint_data, config.ppt_template, output_path)

        print("✅ PowerPoint generated successfully!")
        print(f"   Output: {output_path}")
        print(f"   File size: {os.path.getsize(output_path) / 1024:.2f} KB")
        print()

        print("=" * 70)
        print("Demo completed successfully!")
        print("=" * 70)

        return True

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = demo_markdown_to_ppt()
    sys.exit(0 if success else 1)

