#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Custom tab bar."""


from PyQt5.QtCore import QEvent

from PyQt5.QtGui import QCursor

from PyQt5.QtWidgets import QMenu, QMessageBox, QTabBar


class TabBar(QTabBar):

    """Custom tab bar."""

    def __init__(self, parent=None, *args, **kwargs):
        """Init class custom tab bar."""
        super(TabBar, self).__init__(parent=None, *args, **kwargs)
        self.parent, self.limit = parent, self.count() * 2
        self.menu, self.submenu = QMenu("Tab Options"), QMenu("Tabs")
        self.tab_previews = True
        self.menu.addAction("Tab Menu").setDisabled(True)
        self.menu.addSeparator()
        self.menu.addAction("Top or Bottom Position", self.set_position)
        self.menu.addAction("Undock Tab", self.make_undock)
        self.menu.addAction("Toggle Tabs Previews", self.set_tab_previews)
        self.menu.addMenu(self.submenu)
        self.menu.aboutToShow.connect(self.build_submenu)
        self.tabCloseRequested.connect(
            lambda: self.removeTab(self.currentIndex()))
        self.setMouseTracking(True)
        self.installEventFilter(self)

    def eventFilter(self, obj, event):
        """Custom Events Filder for detecting clicks on Tabs."""
        if obj == self:
            if event.type() == QEvent.MouseMove:
                index = self.tabAt(event.pos())
                self.setCurrentIndex(index)
                return True
            else:
                return QTabBar.eventFilter(self, obj, event)  # False
        else:
            return QMainWindow.eventFilter(self, obj, event)

    def mouseDoubleClickEvent(self, event):
        """Handle double click."""
        self.menu.exec_(QCursor.pos())

    def set_tab_previews(self):
        """Toggle On/Off the Tabs Previews."""
        self.tab_previews = not self.tab_previews
        return self.tab_previews

    def make_undock(self):
        """Undock Tab from TabWidget to a Dialog,if theres more than 2 Tabs."""
        msg = "<b>Needs more than 2 Tabs to allow Un-Dock Tabs !."
        return self.parent.make_undock() if self.count(
            ) > 2 else QMessageBox.warning(self, "Error", msg)

    def set_position(self):
        """Handle set Position on Tabs."""
        self.parent.setTabPosition(0 if self.parent.tabPosition() else 1)

    def build_submenu(self):
        """Handle build a sub-menu on the fly with the list of tabs."""
        self.submenu.clear()
        self.submenu.addAction("Tab list").setDisabled(True)
        for index in tuple(range(self.count())):
            action = self.submenu.addAction("Tab {0}".format(index + 1))
            action.triggered.connect(
                lambda _, index=index: self.setCurrentIndex(index))
