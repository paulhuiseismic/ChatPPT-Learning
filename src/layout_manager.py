from abc import ABC, abstractmethod
from typing import Tuple

from data_structures import SlideContent


class LayoutStrategy(ABC):
    @abstractmethod
    def get_layout(self, slide_content: SlideContent, layout_mapping: dict) -> Tuple[int, str]:
        pass


class TitleOnlyStrategy(LayoutStrategy):
    def get_layout(self, slide_content: SlideContent, layout_mapping: dict) -> Tuple[int, str]:
        layout_name = "Title Only"
        layout_id = layout_mapping.get(layout_name, 1)
        return layout_id, layout_name


class TitleAndContentStrategy(LayoutStrategy):
    def get_layout(self, slide_content: SlideContent, layout_mapping: dict) -> Tuple[int, str]:
        layout_name = "Title and Content"
        layout_id = layout_mapping.get(layout_name, 2)
        return layout_id, layout_name


class titleAndPictureStrategy(LayoutStrategy):
    def get_layout(self, slide_content: SlideContent, layout_mapping: dict) -> Tuple[int, str]:
        layout_name = "Title and Picture"
        layout_id = layout_mapping.get(layout_name, 3)
        return layout_id, layout_name


class TitleContentAndPictureStrategy(LayoutStrategy):
    def get_layout(self, slide_content: SlideContent, layout_mapping: dict) -> Tuple[int, str]:
        layout_name = "Title, Content, and Picture"
        layout_id = layout_mapping.get(layout_name, 4)
        return layout_id, layout_name


class LayoutManager:
    def __init__(self, layout_mapping: dict):
        self.layout_mapping = layout_mapping
        self.strategies = {
            "Title Only": TitleOnlyStrategy(),
            "Title and Content": TitleAndContentStrategy(),
            "Title and Picture": titleAndPictureStrategy(),
            "Title, Content, and Picture": TitleContentAndPictureStrategy(),
        }

    def assign_layout(self, slide_content: SlideContent) -> Tuple[int, str]:
        if slide_content.image_path and slide_content.bullet_points:
            strategy = self.strategies["Title, Content, and Picture"]
        elif slide_content.image_path:
            strategy = self.strategies["Title and Picture"]
        elif slide_content.bullet_points:
            strategy = self.strategies["Title and Content"]
        else:
            strategy = self.strategies["Title Only"]

        return strategy.get_layout(slide_content, self.layout_mapping)