import json
import os.path
from platformdirs import user_config_dir


class Config:
    APP_VERSION = '2.0.15'

    def __init__(self):
        config_path = os.path.join(
            user_config_dir(appname='WaifuCompanion', appauthor='Toshayo', ensure_exists=True),
            'config.json'
        )
        self.active_model = None
        self.other_configs = {}
        self.bypass_window_manager = False
        self.is_click_through = False
        if os.path.exists(config_path):
            with open(config_path, 'r') as config_file:
                config = json.load(config_file)
                if 'activeModelName' in config:
                    self.active_model = config['activeModelName']
                if 'otherConfigs' in config:
                    self.other_configs = config['otherConfigs']
                if 'bypassWindowManager' in config:
                    self.bypass_window_manager = config['bypassWindowManager']
                if 'is_click_through' in config:
                    self.is_click_through = config['is_click_through']

    def save_config(self):
        config_path = os.path.join(
            user_config_dir(appname='WaifuCompanion', appauthor='Toshayo', ensure_exists=True),
            'config.json'
        )
        with open(config_path, 'w') as config_file:
            json.dump({
                'activeModelName': self.active_model,
                'otherConfigs': self.other_configs,
                'bypassWindowManager': self.bypass_window_manager,
                'is_click_through': self.is_click_through
            }, config_file)

    def set_active_model(self, model_name: str):
        self.active_model = model_name
        self.save_config()

    def toggle_click_through(self):
        self.is_click_through = not self.is_click_through
        self.save_config()

    def toggle_bypass_window_manager(self):
        self.bypass_window_manager = not self.bypass_window_manager
        self.save_config()


INSTANCE = Config()
