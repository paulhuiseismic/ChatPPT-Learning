import random
from typing import List, Tuple

from data_structures import SlideContent
from logger import LOG


CONTENT_TYPE_WEIGHTS = {
    "Title": 1,
    "Content": 2,
    "Picture": 4,
}

def calculate_layout_encoding(layout_name: str) -> int:
    parts = layout_name.split(", ")
    base_name = ' '.join(part.split()[0] for part in parts)

    weight_sum = sum(CONTENT_TYPE_WEIGHTS.get(part, 0) for part in base_name.split())

    return weight_sum

def calculate_content_encoding(slide_content: SlideContent) -> int:
    encoding = 0
    if slide_content.title:
        encoding += CONTENT_TYPE_WEIGHTS["Title"]
    if slide_content.bullet_points:
        encoding += CONTENT_TYPE_WEIGHTS["Content"]
    if slide_content.image_path:
        encoding += CONTENT_TYPE_WEIGHTS["Picture"]
    return encoding


class LayoutStrategy:
    def __init__(self, layout_group: List[Tuple[int, str]]):
        self.layout_group = layout_group

    def get_layout(self, slide_content: SlideContent) -> Tuple[int, str]:
        return random.choice(self.layout_group)


class LayoutManager:
    def __init__(self, layout_mapping: dict):
        self.layout_mapping = layout_mapping

        self.strategies = {
            1: self._create_strategy(1),
            3: self._create_strategy(3),
            5: self._create_strategy(5),
            7: self._create_strategy(7),
        }

        LOG.debug(f"LayoutManager initialized with strategies: {self.strategies}")

    def __str__(self):
        output = ["LayoutManager Strategies:"]
        for encoding, strategy in self.strategies.items():
            layout_group = strategy.layout_group
            output.append(f"  Encoding: {encoding}: {len(layout_group)} layouts")
            for layout_id, layout_name in layout_group:
                output.append(f"    - ID: {layout_id}, Name: {layout_name}")
        return "\n".join(output)

    def assign_layout(self, slide_content: SlideContent) -> Tuple[int, str]:
        encoding = calculate_content_encoding(slide_content)

        strategy = self.strategies.get(encoding)
        if not strategy:
            raise ValueError(f"No layout strategy found for encoding: {encoding}")

        return strategy.get_layout(slide_content)


    def _create_strategy(self, layout_type: int) -> LayoutStrategy:
        layout_group = [
            (layout_id, layout_name) for layout_name, layout_id in self.layout_mapping.items()
            if calculate_layout_encoding(layout_name) == layout_type
        ]

        return LayoutStrategy(layout_group)