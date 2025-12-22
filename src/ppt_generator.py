import os
import re
from pptx import Presentation
from utils import remove_all_slides
from logger import LOG


def sanitize_for_xml(text):
    """
    Sanitize text for use in XML by escaping special characters.

    Args:
        text: String that may contain XML special characters

    Returns:
        Sanitized string safe for XML
    """
    if not text:
        return ""

    # Remove or replace problematic characters
    # Keep only alphanumeric, spaces, hyphens, underscores, and dots
    sanitized = re.sub(r'[^\w\s\-_.]', '', text)

    return sanitized


def safe_insert_picture(shape, image_path):
    """
    Safely insert a picture into a placeholder shape.
    Works around XML parsing issues with special characters in image metadata.

    Args:
        shape: The placeholder shape to insert the picture into
        image_path: Path to the image file

    Returns:
        True if successful, False otherwise
    """
    try:
        # The issue is that python-pptx uses the image filename in XML attributes
        # If the filename contains & or other special chars, it causes XML parse errors

        # Get the directory and filename
        directory = os.path.dirname(image_path)
        original_filename = os.path.basename(image_path)
        file_ext = os.path.splitext(original_filename)[1]
        file_base = os.path.splitext(original_filename)[0]

        # Sanitize the base filename for XML safety
        safe_base = sanitize_for_xml(file_base)

        # If sanitization removed everything, use a generic name
        if not safe_base or len(safe_base) < 2:
            safe_base = "image"

        # Create a safe filename
        safe_filename = safe_base + file_ext
        safe_path = os.path.join(directory, safe_filename)

        # If the original path has special characters, create a temporary symlink/copy
        if image_path != safe_path and os.path.exists(image_path):
            import shutil
            # Create a temporary safe copy
            temp_safe_path = os.path.join(directory, f"temp_{safe_filename}")
            shutil.copy2(image_path, temp_safe_path)

            try:
                shape.insert_picture(temp_safe_path)
                LOG.debug(f"Inserted image using safe path: '{temp_safe_path}'")
            finally:
                # Clean up the temporary file
                if os.path.exists(temp_safe_path):
                    try:
                        os.remove(temp_safe_path)
                    except:
                        pass
        else:
            # Path is already safe
            shape.insert_picture(image_path)
            LOG.debug(f"Inserted image: '{image_path}'")

        return True

    except Exception as e:
        LOG.error(f"Error inserting picture '{image_path}': {str(e)}")
        return False


def format_text(paragraph, text):
    while '**' in text:
        start = text.find('**')
        end = text.find('**', start + 2)

        if start != -1 and end != -1:
            if start > 0:
                run = paragraph.add_run()
                run.text = text[:start]

            bold_run = paragraph.add_run()
            bold_run.text = text[start + 2:end]
            bold_run.font.bold = True

            text = text[end + 2:]
        else:
            break

    # Add any remaining text (or all text if no bold markers)
    if text:
        run = paragraph.add_run()
        run.text = text

def generate_presentation(powerpoint_data, template_path: str, output_path: str):
    if not os.path.exists(template_path):
        LOG.error(f"Template path '{template_path}' does not exist")
        raise FileNotFoundError(f"Template file not found: {template_path}")

    prs = Presentation(template_path)
    remove_all_slides(prs)
    prs.core_properties.title = powerpoint_data.title

    for slide in powerpoint_data.slides:
        if slide.layout_id >= len(prs.slide_layouts):
            slide_layout = prs.slide_layouts[0]
        else:
            slide_layout = prs.slide_layouts[slide.layout_id]

        new_slide = prs.slides.add_slide(slide_layout)

        if new_slide.shapes.title:
            new_slide.shapes.title.text = slide.content.title
            LOG.debug(f"New slide title '{new_slide.shapes.title.text}'")

        for shape in new_slide.shapes:
            if shape.has_text_frame and not shape == new_slide.shapes.title:
                text_frame = shape.text_frame
                text_frame.clear()
                for point in slide.content.bullet_points:
                    p = text_frame.add_paragraph()
                    p.level = point['level']
                    format_text(p, point['text'])
                    LOG.debug(f"Add bullet point: '{p.text}' at level {p.level}")
                break

        if slide.content.image_path:
            # Get the project root directory (parent of the directory containing this script)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_dir = os.path.dirname(script_dir)
            image_full_path = os.path.join(project_dir, slide.content.image_path)
            if os.path.exists(image_full_path):
                for shape in new_slide.placeholders:
                    if shape.placeholder_format.type == 18:
                        # Use safe_insert_picture to avoid XML parsing errors
                        if safe_insert_picture(shape, image_full_path):
                            LOG.debug(f"Successfully inserted image: '{image_full_path}'")
                        else:
                            LOG.warning(f"Failed to insert image: '{image_full_path}'")
                        break
            else:
                LOG.warning(f"Image path '{image_full_path}' does not exist. Skipping image insertion.")

    prs.save(output_path)
    LOG.info(f"Presentation saved to '{output_path}'")