import re
import requests
import os

from abc import ABC
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

from azure_openai import chat_model
from langchain_core.prompts import ChatPromptTemplate

from logger import LOG


class ImageAdvisor(ABC):
    def __init__(self, prompt_file='./prompts/image_advisor.txt'):
        self.advisor = None
        self.prompt_file = prompt_file
        self.prompt = self.load_prompt()
        self.create_advisor()

    def load_prompt(self):
        try:
            with open(self.prompt_file, 'r', encoding='utf-8') as file:
                return file.read().strip()
        except FileNotFoundError:
            LOG.error(f"Prompt file not found: {self.prompt_file}")
            raise

    def create_advisor(self):
        chat_prompt = ChatPromptTemplate.from_messages([
            ("system", self.prompt),
            ("human", "**Content**:\n\n{input}"),
        ])

        self.advisor = chat_prompt | chat_model

    def generate_images(self, markdown_content, image_directory="tmps", num_images=3):
        response = self.advisor.invoke({
            "input": markdown_content,
        })

        LOG.debug(f"[Advisor]\m{response.content}")

        keywords = self.get_keywords(response.content)
        image_pair = {}

        for slide_title, query in keywords.items():
            images = self.get_bing_images(slide_title, query, num_images, timeout=1, retries=3)
            if images:
                for image in images:
                    LOG.debug(f"Name: {image['slide_title']}, Query: {image['query']}, Resolution: {image['width']}x{image['height']}")
            else:
                LOG.warning(f"No images found for '{slide_title}'")
                continue

            img = images[0]
            save_directory = f"images/{image_directory}"
            os.makedirs(save_directory, exist_ok=True)
            save_path = os.path.join(save_directory, f"{img['slide_title']}_1.jpeg")
            self.save_image(img["obj"], save_path)
            image_pair[img["slide_title"]] = save_path

        content_with_images = self.insert_images(markdown_content, image_pair)
        return content_with_images, image_pair

    def get_keywords(self, advice):
        pairs = re.findall(r'\[(.+?)\]:\s*(.+)', advice)
        keywords = {key.strip(): value.strip() for key, value in pairs}
        LOG.debug(f"[Advisor keywords]{keywords}")
        return keywords

    def get_bing_images(self, slide_title, query, num_images=5, timeout=1, retries=3):
        url = f"https://www.bing.com/images/search?q={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }

        for attempt in range(retries):
            try:
                response = requests.get(url, headers=headers, timeout=timeout)
                response.raise_for_status()
                break
            except requests.RequestException as e:
                LOG.warning(f"Attempt {attempt + 1}/{retries} failed for '{query}': {e}")
                if attempt == retries - 1:
                    LOG.error(f"All {retries} attempts failed for '{query}'")
                    return []

        soup = BeautifulSoup(response.text, 'html.parser')
        image_elements = soup.select("a.iusc")

        image_links = []
        for img in image_elements:
            m_data = img.get("m")
            if m_data:
                m_json = eval(m_data)
                if "murl" in m_json:
                    image_links.append(m_json["murl"])
            if len(image_links) >= num_images:
                break

        image_data = []
        for link in image_links:
            for attempt in range(retries):
                try:
                    img_data = requests.get(link, headers=headers, timeout=timeout)
                    img = Image.open(BytesIO(img_data.content))
                    image_info = {
                        "slide_title": slide_title,
                        "query": query,
                        "width": img.width,
                        "height": img.height,
                        "resolution": img.width * img.height,
                        "obj": img,
                    }
                    img_data.append(image_info)
                    break
                except Exception as e:
                    LOG.warning(f"Attempt {attempt + 1}/{retries} failed to download image from '{link}': {e}")
                    if attempt == retries - 1:
                        LOG.warning(f"All {retries} attempts failed to download image from '{link}'")
                        if attempt == retries - 1:
                            LOG.error(f"All {retries} attempts failed for '{query}'")

        sorted_images = sorted(image_data, key=lambda x: x["resolution"], reverse=True)
        return sorted_images

    def save_image(self, img, save_path, format="JPEG", quality=85, max_size=1080):
        try:
            width, height = img.size
            if max(width, height) > max_size:
                scaling_factor = max_size / max(width, height)
                new_width = int(width * scaling_factor)
                new_height = int(height * scaling_factor)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            if img.mode == "RGBA":
                format = "PNG"
                save_options = {"optimize": True}
            else:
                save_options = {
                    "quality": quality,
                    "optimize": True,
                    "progressive": True
                }
            img.save(save_path, format=format, **save_options)
            LOG.debug(f"Image saved as {save_path} in {format} format with quality {quality}.")
        except Exception as e:
            LOG.error(f"Error saving image: {e}")

    def insert_images(self, markdown_content, image_pair):
        lines = markdown_content.split("\n")
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            new_lines.append(line)
            if line.startswith('## '):
                slide_title = line[len('## '):].strip()
                if slide_title in image_pair:
                    image_path = image_pair[slide_title]
                    image_markdown = f'![{slide_title}]({image_path})'
                    new_lines.append(image_markdown)
            i += 1
        new_content = "\n".join(new_lines)
        return new_content