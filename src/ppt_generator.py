import os
from pptx import Presentation
from utils import remove_all_slides


def generate_presentation(powerpoint_data, template_path: str, output_path: str):
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template file not found: {template_path}")

    prs = Presentation(template_path)
    remove_all_slides(prs)
    prs.core_properties.title = powerpoint_data.title

    for slide in powerpoint_data.slides:
        if slide.layout >= len(prs.slide_layouts):
            slide_layout = prs.slide_layouts[0]
        else:
            slide_layout = prs.slide_layouts[slide.layout]

        new_slide = prs.slides.add_slide(slide_layout)

        if new_slide.shapes.title:
            new_slide.shapes.title.text = slide.content.title

        for shape in new_slide.shapes:
            if shape.has_text_frame and shape != new_slide.shapes.title:
                text_frame = shape.text_frame
                text_frame.clear()
                for point in slide.content.bullet_points:
                    p = text_frame.add_paragraph()
                    p.text = point
                    p.level = 0
                break

        if slide.content.image_path:
            # Get the project root directory (parent of the directory containing this script)
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_dir = os.path.dirname(script_dir)
            image_full_path = os.path.join(project_dir, slide.content.image_path)
            if os.path.exists(image_full_path):
                for shape in new_slide.placeholders:
                    if shape.placeholder_format.type == 18:
                        shape.insert_picture(image_full_path)
                        break
            else:
                print(f"Warning: Image not found at '{image_full_path}'")

    prs.save(output_path)
    print(f"Presentation saved to '{output_path}'")