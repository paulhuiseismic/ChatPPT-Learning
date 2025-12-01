import re
from typing import Optional, Tuple

from data_structures import PowerPoint
from slide_builder import SlideBuilder
from layout_manager import LayoutManager
from logger import LOG


def parse_input_text(input_text: str, layout_manager: LayoutManager) -> Tuple[PowerPoint, str]:
    lines = input_text.split("\n")
    presentation_title = ""
    slides = []
    slide_builder: Optional[SlideBuilder] = None

    slide_title_pattern = re.compile(r'^##\s+(.*)')
    bullet_pattern = re.compile(r'^-\s+(.*)')
    image_pattern = re.compile(r'!\[.*?\]\((.*?)\)')

    for line in lines:
        line = line.strip()

        if line.startswith('# ') and not line.startswith('##'):
            presentation_title = line[2:].strip()

            first_slide_builder = SlideBuilder(layout_manager)
            first_slide_builder.set_title(presentation_title)
            slide = first_slide_builder.finalize()
            slides.append(slide)

        elif line.startswith('## '):
            match = slide_title_pattern.match(line)
            if match:
                title = match.group(1).strip()
                if slide_builder:
                    slide = slide_builder.finalize()
                    slides.append(slide)
                slide_builder = SlideBuilder(layout_manager)
                slide_builder.set_title(title)

        elif line.startswith('- ') and slide_builder:
            match = bullet_pattern.match(line)
            if match:
                bullet = match.group(1).strip()
                slide_builder.add_bullet_point(bullet)

        elif line.startswith('![') and slide_builder:
            match = image_pattern.match(line)
            if match:
                image_path = match.group(1).strip()
                slide_builder.set_image(image_path)

    if slide_builder:
        slides.append(slide_builder.finalize())

    return PowerPoint(title=presentation_title, slides=slides), presentation_title