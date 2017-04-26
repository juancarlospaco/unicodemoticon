#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Custom tab widget."""


from PyQt5.QtWidgets import (QApplication, QPushButton, QLineEdit, QVBoxLayout,
                             QGridLayout, QGroupBox, QScrollArea, QWidget)


class _ScrollGroup(QScrollArea):

    """Group with Scroll and QVBoxLayout."""

    def __init__(self, title):
        super(_ScrollGroup, self).__init__()
        self.group = QGroupBox(title)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(1)
        self.setWidget(self.group)
        self.group.setLayout(QVBoxLayout())
        self.group.setFlat(True)

    def layout(self):
        return self.group.layout()

    def setLayout(self, layout):
        self.group.setLayout(layout)


class TabSearch(_ScrollGroup):

    """Custom tab widget."""

    def __init__(self, parent=None, *args, **kwargs):
        """Init class custom tab widget."""
        super(TabSearch, self).__init__(self, *args, **kwargs)
        self.parent = parent
        self.setParent(parent)

        search, layout = QLineEdit(self), self.layout()
        search.setPlaceholderText(" Search Unicode...")
        font = search.font()
        font.setPixelSize(25)
        font.setBold(True)
        search.setFont(font)
        search.setFocus()
        layout.addWidget(search)

        self.container, self.buttons, row, index = QWidget(self), [], 0, 0
        self.container.setLayout(QGridLayout())
        layout.addWidget(self.container)
        for i in range(50):
            button = QPushButton("?", self)
            self.buttons.append(button)
            button.released.connect(self.hide)
            button.setFlat(True)
            button.setDisabled(True)
            font = button.font()
            font.setPixelSize(25)
            button.setFont(font)
            index = index + 1  # cant use enumerate()
            row = row + 1 if not index % 8 else row
            self.container.layout().addWidget(button, row, index % 8)
