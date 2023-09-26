import json
import os.path

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QMenu, QAction

import Config
import EventManager
from modelmanager.CompanionModelDefinition import CompanionModelDefinition


class CompanionModelManager(QObject):
    def __init__(self):
        super().__init__()
        self.models: dict[str, CompanionModelDefinition] = {}
        app_dir = os.path.dirname(os.path.abspath(__file__))
        for model in os.scandir(os.path.join(app_dir, '..', 'assets', 'models')):
            if os.path.exists(os.path.join(model.path, 'manifest.json')):
                with open(os.path.join(model.path, 'manifest.json'), 'r') as manifest:
                    model_def = CompanionModelDefinition(model.path, json.load(manifest))
                    self.models[model_def.name] = model_def
        EventManager.INSTANCE.register_listener(EventManager.Events.COMPANION_TRAY_INIT, self.tray_init)

    def on_model_select(self):
        sender: QAction | QObject = self.sender()
        # Checkbox is handled by Qt, override some parts
        if not sender.isChecked():
            sender.setChecked(True)
            return
        action: QAction
        for action in sender.parent().children():
            action.setChecked(False)
        sender.setChecked(True)
        Config.INSTANCE.set_active_model(sender.text())
        EventManager.INSTANCE.fire(self, EventManager.Events.RESTART)

    def tray_init(self, tray_menu: QMenu):
        tray_switch_model_menu = tray_menu.addMenu('Switch model')
        for name, model in self.models.items():
            action = tray_switch_model_menu.addAction(name)
            action.setCheckable(True)
            action.setChecked(Config.INSTANCE.active_model == name)
            action.triggered.connect(self.on_model_select)


INSTANCE = CompanionModelManager()
