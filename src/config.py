import json
import os


class Config:
    def __init__(self, config_file='config.json'):
        self.layout_mapping = None
        self.ppt_template = None
        self.input_mode = None
        self.config_file = config_file
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"Config file '{self.config_file}' not found.")
        
        with open(self.config_file, 'r') as f:
            config = json.load(f)
            
            self.input_mode = config.get('input_mode', 'text')
            
            self.ppt_template = config.get('ppt_template', 'templates/MasterTemplate.pptx')
            
            self.layout_mapping = config.get('layout_mapping', {})