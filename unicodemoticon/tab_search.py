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

    def make_search_unicode(self):
        """Make a search for Unicode Emoticons."""
        sorry = "<i>Nothing found! Search can not find similar Unicode, sorry."
        search = str(QInputDialog.getText(
            None, __doc__, "<b>Type to search Unicode ?:")[0]).lower().strip()
        if search and len(search):
            log.debug("Searching all Unicode for: '{0}'.".format(search))
            emos = [_ for _ in UNICODEMOTICONS.values() if isinstance(_, str)]
            found_exact = [_ for _ in emos if search in _]
            found_by_name = []
            for emoticons_list in emos:
                for emote in emoticons_list:
                    emoticon_name = str(self.get_description(emote)).lower()
                    if search in emoticon_name and len(emoticon_name):
                        found_by_name += emote
            found_tuple = tuple(sorted(set(found_exact + found_by_name)))
            result = found_tuple[:75] if len(found_tuple) else sorry
            msg = """<b>Your Search:</b><h3>{0}</h3><b>{1} Similar Unicode:</b>
            <h1>{2}</h1><i>All Unicode Copied to Clipboard !.""".format(
                search[:99], len(found_tuple), result)
            QApplication.clipboard().setText("".join(found_tuple))
            log.debug("Found Unicode: '{0}'.".format(found_tuple))
            QMessageBox.information(None, __doc__, msg)
            return found_tuple
