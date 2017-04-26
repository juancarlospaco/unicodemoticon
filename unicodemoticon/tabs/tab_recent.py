#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Custom tab widget."""


from PyQt5.QtWidgets import QApplication, QPushButton

from unicodemoticon.core.scrollgroup import ScrollGroup


class TabRecent(ScrollGroup):

    """Custom tab widget."""

    def __init__(self, parent=None, *args, **kwargs):
        """Init class custom tab widget."""
        super(TabRecent, self).__init__(self, *args, **kwargs)
        self.parent = parent
        self.setParent(parent)

        row, index, layout = 0, 0, self.layout()
        self.recent_emoji, self.recent_buttons = str("? " * 50).split(), []
        for i in range(50):
            button = QPushButton("?", self)
            button.released.connect(self.parent.hide)
            button.setFlat(True)
            button.setDisabled(True)
            font = button.font()
            font.setPixelSize(25)
            button.setFont(font)
            index = index + 1  # cant use enumerate()
            row = row + 1 if not index % 8 else row
            self.recent_buttons.append(button)
            layout.addWidget(button, row, index % 8)

    def recentify(self, emote):
        """Update the recent emojis."""
        self.recent_emoji.append(emote)  # append last emoji to last item
        self.recent_emoji.pop(0)  # remove first item
        for index, button in enumerate(self.recent_buttons):
            button.setText(self.recent_emoji[index])
            if str(button.text()) != "?":
                button.pressed.connect(lambda ch=self.recent_emoji[index]:
                                       self.parent.make_preview(str(ch)))
                button.clicked.connect(
                    lambda _, ch=self.recent_emoji[index]:
                        QApplication.clipboard().setText(ch))
                button.setToolTip("<center><h1>{0}<br>{1}".format(
                    self.recent_emoji[index],
                    self.parent.get_description(self.recent_emoji[index])))
                button.setDisabled(False)
        return self.recent_emoji
