import os
import pkgutil
import sys

from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QApplication

import Config
import EventManager
from CompanionWindow import CompanionWindow
from modelmanager import CompanionModelManager


def restart(_):
    global app
    app.quit()
    os.execv(sys.executable, ['python3'] + sys.argv)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    plugins = [__import__('plugins.' + name, fromlist=[''])
               for _, name, _ in pkgutil.iter_modules([os.path.abspath('plugins')])]
    EventManager.INSTANCE.fire(None, EventManager.Events.PLUGINS_INIT)

    if Config.INSTANCE.active_model is None:
        Config.INSTANCE.set_active_model(list(CompanionModelManager.INSTANCE.models.keys())[0])

    window = CompanionWindow(
        app, CompanionModelManager.INSTANCE.models[Config.INSTANCE.active_model]
    )
    window.move(QCursor.pos())
    window.show()

    EventManager.INSTANCE.register_listener(EventManager.Events.RESTART, restart)

    sys.exit(app.exec_())
