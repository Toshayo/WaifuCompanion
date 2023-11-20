from PyQt5.QtCore import Qt, QTimer, QPoint
from PyQt5.QtGui import QIcon, QMouseEvent, QMoveEvent
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QMenu, QSystemTrayIcon, QApplication

from modelmanager.CompanionModelDefinition import CompanionModelDefinition
import Config
import EventManager
from CompanionGraphicsItem import CompanionGraphicsItem


class CompanionWindow(QGraphicsView):
    def __init__(self, app: QApplication, companion_model: CompanionModelDefinition):
        super().__init__()

        self.app = app
        self.companion_model: CompanionModelDefinition = companion_model

        self.delta_x = True

        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet('background:transparent')

        self.tray = QSystemTrayIcon(QIcon('assets/icon.png'), self)
        self.init_tray()

        scene = QGraphicsScene()
        self.companion_graphics_item = CompanionGraphicsItem(
            self.companion_model, self.screen().availableSize()
        )
        scene.addItem(self.companion_graphics_item)
        self.setScene(scene)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.tick)
        self.timer.start(10)

        self.is_mouse_down = False
        self.mouse_initial_position = QPoint(0, 0)

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        EventManager.INSTANCE.fire(self, EventManager.Events.COMPANION_WINDOW_CONSTRUCT)

    def init_tray(self):
        self.tray.activated.connect(lambda: self.setVisible(not self.isVisible()))
        self.tray.setToolTip('Waifu Companion')

        tray_menu = QMenu(self)

        tray_version = tray_menu.addAction('Version : ' + Config.INSTANCE.APP_VERSION)
        tray_version.setDisabled(True)

        EventManager.INSTANCE.fire(tray_menu, EventManager.Events.COMPANION_TRAY_INIT)

        tray_quit_app = tray_menu.addAction('Quit')
        tray_quit_app.triggered.connect(self.app.quit)

        self.tray.setContextMenu(tray_menu)
        self.tray.show()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        # super().mousePressEvent(event)
        self.mouse_initial_position = event.pos()
        self.is_mouse_down = True
        EventManager.INSTANCE.fire(event, EventManager.Events.COMPANION_WINDOW_MOUSE_DOWN)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        # super().mouseReleaseEvent(event)
        self.is_mouse_down = False
        self.companion_model.update_position((self.pos().x(), self.pos().y()))
        EventManager.INSTANCE.fire(event, EventManager.Events.COMPANION_WINDOW_MOUSE_UP)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.move(
            self.pos().x() + event.x() - self.mouse_initial_position.x(),
            self.pos().y() + event.y() - self.mouse_initial_position.y()
        )

    def moveEvent(self, event: QMoveEvent):
        super().moveEvent(event)
        EventManager.INSTANCE.fire(event, EventManager.Events.COMPANION_WINDOW_MOVED)

    def tick(self):
        if self.is_mouse_down:
            return
        screen_size = self.screen().availableGeometry()
        x, y = self.companion_model.get_next_pos(
            (
                screen_size.x(), screen_size.y(),
                screen_size.x() + screen_size.width(), screen_size.y() + screen_size.height()
            ),
            (self.companion_graphics_item.get_model_bounds()),
            (self.pos().x(), self.pos().y())
        )
        if (self.delta_x > 0) != (self.companion_model.speed[0] > 0):
            self.delta_x = self.companion_model.speed[0] > 0
            self.repaint()
        if self.companion_model.frames_count > 1:
            self.repaint()
        self.move(int(x), int(y))
