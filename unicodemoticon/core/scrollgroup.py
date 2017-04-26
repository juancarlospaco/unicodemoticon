#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Group with Scroll and grid."""


from PyQt5.QtWidgets import QGridLayout, QGroupBox, QScrollArea


class ScrollGroup(QScrollArea):

    """Group with Scroll and grid."""

    def __init__(self, title):
        super(ScrollGroup, self).__init__()
        self.group = QGroupBox(title)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(1)
        self.setWidget(self.group)
        self.group.setLayout(QGridLayout())
        self.group.setFlat(True)

    def layout(self):
        return self.group.layout()

    def setLayout(self, layout):
        self.group.setLayout(layout)
