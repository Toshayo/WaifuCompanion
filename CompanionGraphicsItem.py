import typing

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QRectF, QSize
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import QGraphicsItem, QWidget, QStyleOptionGraphicsItem

from modelmanager import CompanionModelManager


class CompanionGraphicsItem(QGraphicsItem):
    def __init__(self, companion_model: CompanionModelManager.CompanionModelDefinition, screen_size: QSize):
        super().__init__()

        self.companion_model = companion_model

        self.waifu = QPixmap()
        self.waifu.load(companion_model.image, "PNG")
        target_height = screen_size.height() * 0.2 * companion_model.scale
        self.model_scale = target_height / (self.waifu.height() / companion_model.sprite_count['h'])
        self.waifu = self.waifu.scaledToHeight(
            int(target_height * companion_model.sprite_count['h']),
            Qt.SmoothTransformation
        )
        self.frames_size = {
            'w': self.waifu.width() / self.companion_model.sprite_count['w'],
            'h': self.waifu.height() / self.companion_model.sprite_count['h']
        }
        self.companion_model.apply_scale(self.model_scale)

    def paint(self, painter: QtGui.QPainter, option: QStyleOptionGraphicsItem,
              widget: typing.Optional[QWidget] = ...) -> None:
        img = self.waifu.copy(QRectF(*self.companion_model.get_next_frame_bounds()).toRect())
        if self.companion_model.is_inverted ^ (self.companion_model.speed[0] < 0):
            img = img.transformed(QTransform().scale(-1, 1), Qt.FastTransformation)
        painter.drawPixmap(
            QRectF(0, 0, self.frames_size['w'], self.frames_size['h']),
            img,
            QRectF(img.rect())
        )

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
            self.frames_size['w'],
            self.frames_size['h']
        )
