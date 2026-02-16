import typing

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRectF, QSize
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QStyleOptionGraphicsItem

import EventManager
from modelmanager.CompanionModelManager import CompanionModelDefinition


class CompanionGraphicsItem(QGraphicsItem):
    def __init__(self, companion_model: CompanionModelDefinition, screen_size: QSize):
        super().__init__()

        self.companion_model = companion_model

        self.waifu = QPixmap()
        self.waifu.load(companion_model.image, "PNG")
        target_height = screen_size.height() * 0.2 * companion_model.scale
        self.model_scale = target_height / (self.waifu.height() / companion_model.sprite_count['h'])
        self.frame_size = {
            'w': round(self.waifu.width() * self.model_scale / self.companion_model.sprite_count['w']),
            'h': round(self.waifu.height() * self.model_scale / self.companion_model.sprite_count['h'])
        }
        self.waifu = self.waifu.scaled(
            self.frame_size['w'] * self.companion_model.sprite_count['w'],
            self.frame_size['h'] * self.companion_model.sprite_count['h'],
            Qt.IgnoreAspectRatio,
            Qt.SmoothTransformation
        )
        self.companion_model.set_frame_size(self.frame_size)

    def paint(self, painter: QtGui.QPainter, option: QStyleOptionGraphicsItem,
              widget: typing.Optional[QWidget] = ...) -> None:
        EventManager.INSTANCE.fire(EventManager.Events.COMPANION_WINDOW_RENDER_PRE, self, painter, option, widget)
        img = self.waifu.copy(QRectF(*self.companion_model.get_next_frame_bounds()).toRect())
        if self.companion_model.should_flip():
            img = img.transformed(QTransform().scale(-1, 1), Qt.FastTransformation)
        animation_offset = self.companion_model.get_sprite_offset()
        painter.drawPixmap(
            QRectF(animation_offset['x'], animation_offset['y'], self.frame_size['w'], self.frame_size['h']),
            img,
            QRectF(img.rect())
        )
        EventManager.INSTANCE.fire(EventManager.Events.COMPANION_WINDOW_RENDER_POST, self, painter, option, widget)

    def get_model_bounds(self) -> tuple[int, int, int, int]:
        return (
            int(self.companion_model.aabb['x'] * self.model_scale),
            int(self.companion_model.aabb['y'] * self.model_scale),
            int(self.companion_model.aabb['width'] * self.model_scale),
            int(self.companion_model.aabb['height'] * self.model_scale)
        )

    def boundingRect(self) -> QRectF:
        return QRectF(
            0, 0,
            self.frame_size['w'],
            self.frame_size['h']
        )
