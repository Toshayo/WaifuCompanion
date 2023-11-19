import json
import os.path
from xdg.BaseDirectory import xdg_config_home


class Config:
    APP_VERSION = '2.0.1'

    def __init__(self):
        config_path = os.path.join(xdg_config_home, 'waifucompanion', 'config.json')
        if os.path.exists(config_path):
            with open(config_path, 'r') as config_file:
                config = json.load(config_file)
                self.active_model = config['activeModelName'] if 'activeModelName' in config \
                    else None
                self.other_configs = {}

    def save_config(self):
        config_path = os.path.join(xdg_config_home, 'waifucompanion', 'config.json')
        with open(config_path, 'w') as config_file:
            json.dump({
                'activeModelName': self.active_model,
                'otherConfigs': self.other_configs
            }, config_file)

    def set_active_model(self, model_name: str):
        self.active_model = model_name
        self.save_config()


INSTANCE = Config()
