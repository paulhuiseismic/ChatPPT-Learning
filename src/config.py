import json
import os


class Config:
    def __init__(self, config_file='config.json'):
        self.image_advisor_prompt = None
        self.content_assistant_prompt = None
        self.content_formatter_prompt = None
        self.input_mode = None
        self.ppt_template = None
        self.chatbot_prompt = None
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file '{self.config_file}' not found.")
        
        with open(self.config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            
            self.input_mode = config.get('input_mode', 'text')
            
            self.ppt_template = config.get('ppt_template', 'templates/MasterTemplate.pptx')
            
            self.chatbot_prompt = config.get('chatbot_prompt', '')
            
            self.content_formatter_prompt = config.get('content_formatter_prompt', '')
            self.content_assistant_prompt = config.get('content_assistant_prompt', '')
            self.image_advisor_prompt = config.get('image_advisor_prompt', '')