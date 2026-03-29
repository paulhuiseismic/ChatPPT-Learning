import json
import re
import requests
import os
import time

from abc import ABC
from bs4 import BeautifulSoup
from PIL import Image as PILImage
from io import BytesIO
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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
        """
        Generate images for slides in markdown content

        Args:
            markdown_content: Markdown text with ## headers for slides
            image_directory: Directory to save images
            num_images: Number of images to try downloading per slide

        Returns:
            Tuple of (enhanced_content, image_pair_dict)
        """
        LOG.info(f"Starting image generation for content with {len(markdown_content)} characters")

        # Get AI recommendations for image keywords
        response = self.advisor.invoke({
            "input": markdown_content,
        })

        LOG.debug(f"[Advisor response]\n{response.content}")

        # Extract keywords from AI response
        keywords = self.get_keywords(response.content)

        if not keywords:
            LOG.error("No keywords extracted from advisor response. Cannot proceed with image search.")
            return markdown_content, {}

        LOG.info(f"Extracted {len(keywords)} slide titles with keywords")

        image_pair = {}

        for slide_title, query in keywords.items():
            LOG.info(f"Processing slide: '{slide_title}' with query: '{query}'")

            images = self.get_bing_images(slide_title, query, num_images, timeout=10, retries=3)

            if images:
                LOG.info(f"Found {len(images)} images for '{slide_title}'")
                for idx, image in enumerate(images[:3]):  # Log top 3
                    LOG.debug(f"  Image {idx+1}: {image['width']}x{image['height']} ({image['resolution']:,} pixels)")
            else:
                LOG.warning(f"No images found for '{slide_title}' with query '{query}'")
                continue

            # Use the highest resolution image
            img = images[0]
            save_directory = f"images/{image_directory}"
            os.makedirs(save_directory, exist_ok=True)
            save_path = os.path.join(save_directory, f"{img['slide_title']}_1.jpeg")

            self.save_image(img["obj"], save_path)
            image_pair[img["slide_title"]] = save_path
            LOG.info(f"Saved image for '{slide_title}' to {save_path}")

        LOG.info(f"Image generation complete. Added {len(image_pair)} images.")

        # Insert images into markdown
        content_with_images = self.insert_images(markdown_content, image_pair)
        return content_with_images, image_pair

    def get_keywords(self, advice):
        """
        Extract keywords from advisor response.
        Handles multiple formats:
        - [Slide Title]: keyword
        - Slide Title: keyword
        - ## Slide Title: keyword
        """
        LOG.debug(f"[Advisor raw response]\n{advice}")

        # Try pattern 1: [Title]: keyword
        pairs = re.findall(r'\[(.+?)\]:\s*(.+)', advice)

        # Try pattern 2: Title: keyword (without brackets)
        if not pairs:
            pairs = re.findall(r'^([^:\n]+):\s*(.+)$', advice, re.MULTILINE)

        # Try pattern 3: Extract from lines containing ':'
        if not pairs:
            lines = advice.strip().split('\n')
            pairs = []
            for line in lines:
                if ':' in line:
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        # Remove common prefixes like [, ], ##, -, *
                        key = parts[0].strip().strip('[]#-*').strip()
                        value = parts[1].strip()
                        if key and value:
                            pairs.append((key, value))

        keywords = {key.strip(): value.strip() for key, value in pairs}
        LOG.debug(f"[Advisor extracted keywords] {keywords}")

        if not keywords:
            LOG.warning(f"[Advisor] No keywords extracted from response. Response format may be incorrect.")
            LOG.warning(f"[Advisor] Expected format: [Slide Title]: search keyword")

        return keywords

    def get_bing_images(self, slide_title, query, num_images=5, timeout=10, retries=3, max_attempts=15):
        """
        从 Bing 搜索图像并返回图像数据

        Args:
            slide_title: 幻灯片标题
            query: 搜索关键词
            num_images: 需要的图像数量
            timeout: 请求超时时间(秒)
            retries: 重试次数
            max_attempts: 最大尝试次数（考虑到有些图片可能下载失败）
        """
        url = f"https://www.bing.com/images/search?q={query}"

        # 添加完整的浏览器请求头
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0"
        }

        # 配置 Session 和重试策略
        session = requests.Session()
        retry_strategy = Retry(
            total=retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        try:
            # 发送请求获取搜索结果页面
            response = session.get(url, headers=headers, timeout=15)

            if response.status_code != 200:
                LOG.error(f"Error fetching Bing search page for '{query}': HTTP {response.status_code}")
                return []
        except Exception as e:
            LOG.error(f"Failed to fetch Bing search page for '{query}': {e}")
            return []

        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        image_elements = soup.select("a.iusc")

        # 提取图像链接
        image_links = []
        for img in image_elements:
            m_data = img.get("m")
            if m_data:
                try:
                    m_json = json.loads(m_data)
                    if "murl" in m_json:
                        image_links.append(m_json["murl"])
                except (json.JSONDecodeError, KeyError, TypeError) as e:
                    LOG.debug(f"Failed to parse image metadata: {e}")
                    continue
            # 获取更多链接以备用（因为有些可能下载失败）
            if len(image_links) >= max_attempts:
                break

        LOG.info(f"Found {len(image_links)} image links for '{query}'")

        # 下载图像并获取分辨率
        image_data = []
        successful_downloads = 0

        for idx, link in enumerate(image_links):
            # 如果已经获取到足够的图像，停止
            if successful_downloads >= num_images:
                break

            try:
                # 添加小延迟避免请求过快
                if idx > 0:
                    time.sleep(0.3)

                # 下载图像，使用更短的超时时间
                img_data = session.get(
                    link,
                    headers=headers,
                    timeout=(5, timeout),  # (连接超时, 读取超时)
                    stream=True
                )

                # 检查响应状态
                if img_data.status_code != 200:
                    LOG.debug(f"Skipping {link}: HTTP {img_data.status_code}")
                    continue

                # 限制下载大小并打开图像
                img_data.raw.decode_content = True
                img = PILImage.open(BytesIO(img_data.content))

                # 验证图像有效性
                img.verify()
                # 重新打开图像（verify 后需要重新加载）
                img = PILImage.open(BytesIO(img_data.content))

                # 将信息存储为字典
                image_info = {
                    "slide_title": slide_title,
                    "query": query,
                    "width": img.width,
                    "height": img.height,
                    "resolution": img.width * img.height,
                    "obj": img,
                }
                image_data.append(image_info)
                successful_downloads += 1
                LOG.debug(f"Successfully downloaded image {successful_downloads}/{num_images}: {img.width}x{img.height}")

            except requests.exceptions.Timeout:
                LOG.debug(f"Timeout (skipping): {link[:80]}...")
                continue
            except requests.exceptions.ConnectionError:
                LOG.debug(f"Connection error (skipping): {link[:80]}...")
                continue
            except requests.exceptions.RequestException as e:
                LOG.debug(f"Request error (skipping): {str(e)[:80]}...")
                continue
            except Exception as e:
                LOG.debug(f"Failed to process image (skipping): {str(e)[:80]}...")
                continue

        # 关闭 session
        session.close()

        # 按分辨率从大到小排序
        sorted_images = sorted(image_data, key=lambda x: x["resolution"], reverse=True)

        LOG.info(f"Successfully retrieved {len(sorted_images)} images for '{query}'")
        return sorted_images

    def save_image(self, img, save_path, format="JPEG", quality=85, max_size=1080):
        """
        Save image with format conversion and resizing

        Args:
            img: PIL Image object
            save_path: Path to save the image
            format: Image format (JPEG or PNG)
            quality: JPEG quality (1-100)
            max_size: Maximum dimension for resizing
        """
        try:
            # Convert image mode if necessary
            if img.mode in ('P', 'LA', 'PA'):
                # Palette mode or alpha modes need conversion
                img = img.convert('RGB')
                LOG.debug(f"Converted image mode from {img.mode} to RGB")
            elif img.mode == 'RGBA':
                # RGBA should be saved as PNG, not JPEG
                format = "PNG"
                # Or convert to RGB with white background
                if save_path.lower().endswith('.jpeg') or save_path.lower().endswith('.jpg'):
                    background = PILImage.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])  # 3 is the alpha channel
                    img = background
                    format = "JPEG"
                    LOG.debug("Converted RGBA to RGB with white background for JPEG")
            elif img.mode not in ('RGB', 'L'):
                # Convert any other mode to RGB
                img = img.convert('RGB')
                LOG.debug(f"Converted image mode to RGB")

            # Resize if needed
            width, height = img.size
            if max(width, height) > max_size:
                scaling_factor = max_size / max(width, height)
                new_width = int(width * scaling_factor)
                new_height = int(height * scaling_factor)
                img = img.resize((new_width, new_height), PILImage.Resampling.LANCZOS)
                LOG.debug(f"Resized image from {width}x{height} to {new_width}x{new_height}")

            # Set save options based on format
            if format == "PNG":
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
            LOG.error(f"Error saving image to {save_path}: {e}")
            import traceback
            traceback.print_exc()

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