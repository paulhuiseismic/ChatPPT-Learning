import re
from typing import Optional, Tuple

from data_structures import PowerPoint
from slide_builder import SlideBuilder
from layout_manager import LayoutManager
from logger import LOG


def parse_bullet_point_level(line: str) -> Tuple[int, str]:
    indent_length = len(line) - len(line.lstrip())

    indent_level = indent_length // 2

    LOG.debug(f"Indent level: {indent_level}")
    LOG.debug(f"Line: {line}")

    bullet_text = line.strip().lstrip('- ').strip()
    return indent_level, bullet_text


def parse_input_text(input_text: str, layout_manager: LayoutManager) -> Tuple[PowerPoint, str]:
    lines = input_text.split("\n")
    presentation_title = ""
    slides = []
    slide_builder: Optional[SlideBuilder] = None

    slide_title_pattern = re.compile(r'^##\s+(.*)')
    bullet_pattern = re.compile(r'^(\s*)-\s+(.*)')
    image_pattern = re.compile(r'!\[.*?\]\((.*?)\)')

    for line in lines:
        if line.strip() == '':
            continue

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

        elif bullet_pattern.match(line) and slide_builder:
            match = bullet_pattern.match(line)
            if match:
                indent_spaces, bullet = match.groups()
                indent_level = len(indent_spaces) // 2
                bullet_text = bullet.strip()
                slide_builder.add_bullet_point(bullet_text, level=indent_level)

        elif line.startswith('![') and slide_builder:
            match = image_pattern.match(line)
            if match:
                image_path = match.group(1).strip()
                slide_builder.set_image(image_path)

    if slide_builder:
        slides.append(slide_builder.finalize())

    return PowerPoint(title=presentation_title, slides=slides), presentation_title