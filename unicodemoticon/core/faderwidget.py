#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Custom Placeholder Fading Widget for tabs on TabWidget."""


from PyQt5.QtCore import QTimeLine

from PyQt5.QtGui import QPainter

from PyQt5.QtWidgets import QLabel


class FaderWidget(QLabel):

    """Custom Placeholder Fading Widget for tabs on TabWidget."""

    def __init__(self, parent):
        """Init class."""
        super(FaderWidget, self).__init__(parent)
        self.timeline, self.opacity, self.old_pic = QTimeLine(), 1.0, None
        self.timeline.valueChanged.connect(self.animate)
        self.timeline.finished.connect(self.close)
        self.timeline.setDuration(750)  # 500 ~ 750 Ms is Ok, Not more.

    def paintEvent(self, event):
        """Overloaded paintEvent to set opacity and pic."""
        painter = QPainter(self)
        painter.setOpacity(self.opacity)
        if self.old_pic:
            painter.drawPixmap(0, 0, self.old_pic)

    def animate(self, value):
        """Animation of Opacity."""
        self.opacity = 1.0 - value
        return self.hide() if self.opacity < 0.1 else self.repaint()

    def fade(self, old_pic, old_geometry, move_to):
        """Fade from previous tab to new tab."""
        if self.isVisible():
            self.close()
        if self.timeline.state():
            self.timeline.stop()
        self.setGeometry(old_geometry)
        self.move(1, move_to)
        self.old_pic = old_pic
        self.timeline.start()
        self.show()
