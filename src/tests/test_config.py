"""
Unit tests for config module
"""
import unittest
import sys
import os
import json
import tempfile

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import Config


class TestConfig(unittest.TestCase):
    """Test cases for Config class"""

    def test_config_file_not_found(self):
        """Test loading non-existent config file"""
        with self.assertRaises(FileNotFoundError):
            Config(config_file='nonexistent.json')

    def test_config_loading(self):
        """Test loading config from file"""
        # Create a temporary config file
        config_data = {
            'input_mode': 'markdown',
            'ppt_template': 'templates/TestTemplate.pptx',
            'chatbot_prompt': 'prompts/chatbot.txt',
            'content_formatter_prompt': 'prompts/formatter.txt',
            'content_assistant_prompt': 'prompts/assistant.txt',
            'image_advisor_prompt': 'prompts/advisor.txt'
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_config_path = f.name

        try:
            config = Config(config_file=temp_config_path)

            self.assertEqual(config.input_mode, 'markdown')
            self.assertEqual(config.ppt_template, 'templates/TestTemplate.pptx')
            self.assertEqual(config.chatbot_prompt, 'prompts/chatbot.txt')
            self.assertEqual(config.content_formatter_prompt, 'prompts/formatter.txt')
            self.assertEqual(config.content_assistant_prompt, 'prompts/assistant.txt')
            self.assertEqual(config.image_advisor_prompt, 'prompts/advisor.txt')
        finally:
            os.unlink(temp_config_path)

    def test_config_default_values(self):
        """Test config with default values"""
        config_data = {}

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_config_path = f.name

        try:
            config = Config(config_file=temp_config_path)

            self.assertEqual(config.input_mode, 'text')
            self.assertEqual(config.ppt_template, 'templates/MasterTemplate.pptx')
            self.assertEqual(config.chatbot_prompt, '')
        finally:
            os.unlink(temp_config_path)

    def test_config_partial_values(self):
        """Test config with partial values"""
        config_data = {
            'input_mode': 'docx',
            'ppt_template': 'custom/template.pptx'
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(config_data, f)
            temp_config_path = f.name

        try:
            config = Config(config_file=temp_config_path)

            self.assertEqual(config.input_mode, 'docx')
            self.assertEqual(config.ppt_template, 'custom/template.pptx')
            self.assertEqual(config.chatbot_prompt, '')
        finally:
            os.unlink(temp_config_path)


    def test_config_unicode_values(self):
        """Test loading config file with non-ASCII (Unicode) values"""
        config_data = {
            'input_mode': 'text',
            'ppt_template': 'templates/模板.pptx',
            'chatbot_prompt': '提示词/chatbot.txt',
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', encoding='utf-8', delete=False) as f:
            json.dump(config_data, f, ensure_ascii=False)
            temp_config_path = f.name

        try:
            config = Config(config_file=temp_config_path)
            self.assertEqual(config.ppt_template, 'templates/模板.pptx')
            self.assertEqual(config.chatbot_prompt, '提示词/chatbot.txt')
        finally:
            os.unlink(temp_config_path)


if __name__ == '__main__':
    unittest.main()
