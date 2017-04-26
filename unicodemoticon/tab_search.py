#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Custom tab widget."""


from PyQt5.QtCore import QTimer

from PyQt5.QtWidgets import (QApplication, QPushButton, QLineEdit, QVBoxLayout,
                             QGridLayout, QGroupBox, QScrollArea, QWidget)

from .data import UNICODEMOTICONS


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
        return self.group.setLayout(layout)


class TabSearch(_ScrollGroup):

    """Custom tab widget."""

    def __init__(self, parent=None, *args, **kwargs):
        """Init class custom tab widget."""
        super(TabSearch, self).__init__(self, *args, **kwargs)
        self.parent = parent
        self.setParent(parent)

        # Timer to start
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self._make_search_unicode)

        self.search, layout = QLineEdit(self), self.layout()
        self.search.setPlaceholderText(" Search Unicode . . .")
        font = self.search.font()
        font.setPixelSize(25)
        font.setBold(True)
        self.search.setFont(font)
        self.search.setFocus()
        self.search.textChanged.connect(self._go)
        layout.addWidget(self.search)

        self.container, self.searchbutons, row, index = QWidget(self), [], 0, 0
        self.container.setLayout(QGridLayout())
        layout.addWidget(self.container)
        for i in range(50):
            button = QPushButton("?", self)
            button.released.connect(self.hide)
            button.setFlat(True)
            button.setDisabled(True)
            font = button.font()
            font.setPixelSize(25)
            button.setFont(font)
            index = index + 1  # cant use enumerate()
            row = row + 1 if not index % 8 else row
            self.searchbutons.append(button)
            self.container.layout().addWidget(button, row, index % 8)

    def _go(self):
        """Run/Stop the QTimer."""
        if self.timer.isActive():
            self.timer.stop()
        return self.timer.start(1000)

    def _make_search_unicode(self):
        """Make a search for Unicode Emoticons."""
        search = str(self.search.text()).lower().strip()
        if search and len(search):
            emos = [_ for _ in UNICODEMOTICONS.values() if isinstance(_, str)]
            found_exact = [_ for _ in emos if search in _]
            found_by_name = []
            for emoticons_list in emos:
                for emote in emoticons_list:
                    emojiname = str(self.parent.get_description(emote)).lower()
                    if search in emojiname and len(emojiname):
                        found_by_name += emote
            results = tuple(sorted(set(found_exact + found_by_name)))[:50]
            for emoji, button in zip(results, self.searchbutons):
                button.setText(emoji)
                button.pressed.connect(lambda ch=emoji:
                                       self.parent.make_preview(ch))
                button.clicked.connect(
                    lambda _, ch=emoji: QApplication.clipboard().setText(ch))
                button.setToolTip("<center><h1>{0}<br>{1}".format(
                    emoji, self.parent.get_description(emoji)))
                button.setDisabled(False)
            return results
