import json
import os.path
from platformdirs import user_config_dir


class Config:
    APP_VERSION = '2.0.12'

    def __init__(self):
        config_path = os.path.join(
            user_config_dir(appname='WaifuCompanion', appauthor='Toshayo', ensure_exists=True),
            'config.json'
        )
        self.active_model = None
        self.other_configs = {}
        self.bypass_window_manager = True
        if os.path.exists(config_path):
            with open(config_path, 'r') as config_file:
                config = json.load(config_file)
                if 'activeModelName' in config:
                    self.active_model = config['activeModelName']
                if 'otherConfigs' in config:
                    self.other_configs = config['otherConfigs']
                if 'bypassWindowManager' in config:
                    self.bypass_window_manager = config['bypassWindowManager']

    def save_config(self):
        config_path = os.path.join(
            user_config_dir(appname='WaifuCompanion', appauthor='Toshayo', ensure_exists=True),
            'config.json'
        )
        with open(config_path, 'w') as config_file:
            json.dump({
                'activeModelName': self.active_model,
                'otherConfigs': self.other_configs,
                'bypassWindowManager': self.bypass_window_manager
            }, config_file)

    def set_active_model(self, model_name: str):
        self.active_model = model_name
        self.save_config()


INSTANCE = Config()
