#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""UnicodEmoticons."""


import logging as log

import unicodedata

from webbrowser import open_new_tab

from PyQt5.QtCore import Qt, QTimer

from PyQt5.QtGui import QCursor, QIcon

from PyQt5.QtWidgets import (QApplication, QDesktopWidget, QDialog,
                             QInputDialog, QLabel, QMenu, QMessageBox,
                             QPushButton, QSystemTrayIcon, QTabWidget,
                             QToolButton, QVBoxLayout)

from unicodemoticon.core.faderwidget import FaderWidget
from unicodemoticon.core.tabbar import TabBar
from unicodemoticon.core.scrollgroup import ScrollGroup
from unicodemoticon.core.data import (STD_ICON_NAMES, UNICODEMOTICONS,
                                      AUTOSTART_DESKTOP_FILE)

from unicodemoticon.tabs.tab_html import TabHtml
from unicodemoticon.tabs.tab_symbols import TabSymbols
from unicodemoticon.tabs.tab_tool import TabTool
from unicodemoticon.tabs.tab_recent import TabRecent
from unicodemoticon.tabs.tab_search import TabSearch

from anglerfish import set_desktop_launcher


__version__ = '3.0.0'
__license__ = ' GPLv3+ LGPLv3+ '
__author__ = ' Juan Carlos '
__email__ = 'juancarlospaco@gmail.com'
__url__ = 'https://github.com/juancarlospaco/unicodemoticon#unicodemoticon'
__all__ = ("MainWidget", )


##############################################################################


class MainWidget(QTabWidget):

    """Custom main widget."""

    def __init__(self, parent=None, *args, **kwargs):
        """Init class custom tab widget."""
        super(MainWidget, self).__init__(parent=None, *args, **kwargs)
        self.parent = parent
        self.setTabBar(TabBar(self))
        self.setMovable(False)
        self.setTabsClosable(False)
        self.setTabShape(QTabWidget.Triangular)
        self.init_preview()
        self.init_corner_menus()
        self.init_tray()
        self.addTab(TabSearch(self), "Search")
        self.addTab(TabTool(self), "Tools")
        self.addTab(TabHtml(self), "HTML")
        self.addTab(TabSymbols(self), "Symbols")
        self._recent_tab = TabRecent(self)
        self.recentify = self._recent_tab.recentify  # shortcut
        self.addTab(self._recent_tab, "Recent")
        self.widgets_to_tabs(self.json_to_widgets(UNICODEMOTICONS))
        self.make_trayicon()
        self.setMinimumSize(QDesktopWidget().screenGeometry().width() // 1.5,
                            QDesktopWidget().screenGeometry().height() // 1.5)
        # self.showMaximized()

    def init_preview(self):
        self.previews, self.timer = [], QTimer(self)
        self.fader, self.previous_pic = FaderWidget(self), None
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(lambda: [_.close() for _ in self.previews])
        self.taimer, self.preview = QTimer(self), QLabel("Preview")
        self.taimer.setSingleShot(True)
        self.taimer.timeout.connect(lambda: self.preview.hide())
        font = self.preview.font()
        font.setPixelSize(100)
        self.preview.setFont(font)
        self.preview.setDisabled(True)
        self.preview.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.preview.setAttribute(Qt.WA_TranslucentBackground, True)

    def init_corner_menus(self):
        self.menu_1, self.menu_0 = QToolButton(self), QToolButton(self)
        self.menu_1.setText(" ⚙ ")
        self.menu_1.setToolTip("<b>Options, Extras")
        self.menu_0.setText(" ? ")
        self.menu_0.setToolTip("<b>Help, Info")
        font = self.menu_1.font()
        font.setBold(True)
        self.menu_1.setFont(font)
        self.menu_0.setFont(font)
        self.menu_tool, self.menu_help = QMenu("Tools Extras"), QMenu("Help")
        self.menu_tool.addAction(" Tools & Extras ").setDisabled(True)
        self.menu_help.addAction(" Help & Info ").setDisabled(True)
        self.menu_0.setMenu(self.menu_help)
        self.menu_1.setMenu(self.menu_tool)
        self.menu_tool.addAction("Explain Unicode", self.make_explain_unicode)
        self.menu_tool.addAction("Alternate Case Clipboard",
                                 self.alternate_clipboard)
        self.menu_tool.addSeparator()
        self.menu_tool.addAction("AutoCenter Window", self.center)
        self.menu_tool.addAction("Set Icon", self.set_icon)
        self.menu_tool.addAction(  # force recreate desktop file
            "Add Launcher to Desktop", lambda: set_desktop_launcher(
                "unicodemoticon", AUTOSTART_DESKTOP_FILE, True))
        self.menu_tool.addAction("Move to Mouse position",
                                 self.move_to_mouse_position)
        self.menu_tool.addSeparator()
        self.menu_tool.addAction("Minimize", self.showMinimized)
        self.menu_tool.addAction("Hide", self.hide)
        self.menu_tool.addAction("Quit", exit)
        self.menu_help.addAction("About Qt 5",
                                 lambda: QMessageBox.aboutQt(None))
        self.menu_help.addAction("About Unicodemoticon",
                                 lambda: open_new_tab(__url__))
        self.setCornerWidget(self.menu_1, 1)
        self.setCornerWidget(self.menu_0, 0)
        self.currentChanged.connect(self.make_tabs_previews)
        self.currentChanged.connect(self.make_tabs_fade)

    def init_tray(self):
        self.tray, self.menu = QSystemTrayIcon(self), QMenu(__doc__)
        self.menu.addAction("    Emoticons").setDisabled(True)
        self.menu.setIcon(self.windowIcon())
        self.menu.addSeparator()
        self.menu.setProperty("emoji_menu", True)
        list_of_labels = sorted(UNICODEMOTICONS.keys())  # menus
        menus = [self.menu.addMenu(_.title()) for _ in list_of_labels]
        self.menu.addSeparator()
        log.debug("Building Emoticons SubMenus.")
        for item, label in zip(menus, list_of_labels):
            item.setStyleSheet("padding:0;margin:0;border:0;menu-scrollable:1")
            font = item.font()
            font.setPixelSize(20)
            item.setFont(font)
            self.build_submenu(UNICODEMOTICONS[label.lower()], item)
        self.menu.addSeparator()
        self.menu.addAction("Alternate Case Clipboard",
                            self.alternate_clipboard)
        self.menu.addSeparator()
        self.menu.addAction("Quit", exit)
        self.menu.addAction("Show", self.showMaximized)
        self.menu.addAction("Minimize", self.showMinimized)
        self.tray.setContextMenu(self.menu)

    def build_submenu(self, char_list: (str, tuple), submenu: QMenu) -> QMenu:
        """Take a list of characters and a submenu and build actions on it."""
        submenu.setProperty("emoji_menu", True)
        submenu.setWindowOpacity(0.9)
        submenu.setToolTipsVisible(True)
        for _char in sorted(char_list):
            action = submenu.addAction(_char.strip())
            action.setToolTip(self.get_description(_char))
            action.hovered.connect(lambda _, ch=_char: self.make_preview(ch))
            action.triggered.connect(
                lambda _, char=_char: QApplication.clipboard().setText(char))
        return submenu

    def make_trayicon(self):
        """Make a Tray Icon."""
        if self.windowIcon() and __doc__:
            self.tray.setIcon(self.windowIcon())
            self.tray.setToolTip(__doc__)
            self.tray.activated.connect(
                lambda: self.hide() if self.isVisible()
                else self.showMaximized())
            return self.tray.show()

    def make_explain_unicode(self) -> tuple:
        """Make an explanation from unicode entered,if at least 1 chars."""
        explanation, uni = "", None
        uni = str(QInputDialog.getText(
            None, __doc__, "<b>Type Unicode character to explain?")[0]).strip()
        if uni and len(uni):
            explanation = ", ".join([self.get_description(_) for _ in uni])
            QMessageBox.information(None, __doc__, str((uni, explanation)))
        log.debug((uni, explanation))
        return (uni, explanation)

    def alternate_clipboard(self) -> str:
        """Make alternating camelcase clipboard."""
        return QApplication.clipboard().setText(
            self.make_alternate_case(str(QApplication.clipboard().text())))

    def make_alternate_case(self, stringy: str) -> str:
        """Make alternating camelcase string."""
        return "".join([_.lower() if i % 2 else _.upper()
                        for i, _ in enumerate(stringy)])

    def get_description(self, emote: str):
        description = ""
        try:
            description = unicodedata.name(str(emote).strip()).title()
        except ValueError:
            log.debug("Description not found for Unicode: " + emote)
        finally:
            return description

    def make_preview(self, emoticon_text: str):
        """Make Emoticon Previews for the current Hovered one."""
        log.debug(emoticon_text)
        if self.taimer.isActive():  # Be Race Condition Safe
            self.taimer.stop()
        self.preview.setText(" " + emoticon_text + " ")
        self.preview.move(QCursor.pos())
        self.preview.show()
        self.taimer.start(1000)  # how many time display the previews

    def json_to_widgets(self, jotason: dict):
        """Take a json string object return QWidgets."""
        dict_of_widgets, row = {}, 0
        for titlemotes in tuple(sorted(jotason.items())):
            tit = str(titlemotes[0]).strip()[:9].title()
            area = ScrollGroup(tit)
            layout = area.layout()

            grid_cols = 2 if tit.lower() == "multichar" else 8
            for index, emote in enumerate(tuple(set(list(titlemotes[1])))):
                button = QPushButton(emote, self)
                button.clicked.connect(lambda _, c=emote:
                                       QApplication.clipboard().setText(c))
                button.released.connect(self.hide)
                button.released.connect(lambda c=emote: self.recentify(c))
                button.pressed.connect(lambda c=emote: self.make_preview(c))
                button.setToolTip("<center><h1>{0}<br>{1}".format(
                    emote, self.get_description(emote)))
                button.setFlat(True)
                font = button.font()
                font.setPixelSize(50)
                button.setFont(font)
                row = row + 1 if not index % grid_cols else row
                layout.addWidget(button, row, index % grid_cols)

            dict_of_widgets[tit] = area
        return dict_of_widgets

    def widgets_to_tabs(self, dict_of_widgets: dict):
        """Take a dict of widgets and build tabs from them."""
        for title, widget in tuple(sorted(dict_of_widgets.items())):
            self.addTab(widget, title)

    def center(self):
        """Center Window on the Current Screen,with Multi-Monitor support."""
        self.showNormal()
        self.resize(QDesktopWidget().screenGeometry().width() // 1.5,
                    QDesktopWidget().screenGeometry().height() // 1.5)
        window_geometry = self.frameGeometry()
        mousepointer_position = QApplication.desktop().cursor().pos()
        screen = QApplication.desktop().screenNumber(mousepointer_position)
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        window_geometry.moveCenter(centerPoint)
        return bool(not self.move(window_geometry.topLeft()))

    def move_to_mouse_position(self):
        """Center the Window on the Current Mouse position."""
        self.showNormal()
        self.resize(QDesktopWidget().screenGeometry().width() // 1.5,
                    QDesktopWidget().screenGeometry().height() // 1.5)
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(QApplication.desktop().cursor().pos())
        return bool(not self.move(window_geometry.topLeft()))

    def set_icon(self, icon: (None, str)=None) -> str:
        """Return a string with opendesktop standard icon name for Qt."""
        if not icon:
            try:
                cur_idx = STD_ICON_NAMES.index(self.windowIcon().name())
            except ValueError:
                cur_idx = 0
            icon = QInputDialog.getItem(None, __doc__, "<b>Choose Icon name?:",
                                        STD_ICON_NAMES, cur_idx, False)[0]
        if icon:
            log.debug("Setting Tray and Window Icon name to:{}.".format(icon))
            self.tray.setIcon(QIcon.fromTheme("{}".format(icon)))
            self.setWindowIcon(QIcon.fromTheme("{}".format(icon)))
        return icon

    def make_tabs_fade(self, index):
        """Make tabs fading transitions."""
        self.fader.fade(
            self.previous_pic, self.widget(index).geometry(),
            1 if self.tabPosition() else self.tabBar().tabRect(0).height())
        self.previous_pic = self.currentWidget().grab()

    def make_undock(self):
        """Undock a Tab from TabWidget and promote to a Dialog."""
        dialog, index = QDialog(self), self.currentIndex()
        widget_from_tab = self.widget(index)
        dialog_layout = QVBoxLayout(dialog)
        dialog.setWindowTitle(self.tabText(index))
        dialog.setToolTip(self.tabToolTip(index))
        dialog.setWhatsThis(self.tabWhatsThis(index))
        dialog.setWindowIcon(self.tabIcon(index))
        dialog.setFont(widget_from_tab.font())
        dialog.setStyleSheet(widget_from_tab.styleSheet())
        dialog.setMinimumSize(widget_from_tab.minimumSize())
        dialog.setMaximumSize(widget_from_tab.maximumSize())
        dialog.setGeometry(widget_from_tab.geometry())

        def closeEvent_override(event):
            """Re-dock back from Dialog to a new Tab."""
            msg = "<b>Close this Floating Tab Window and Re-Dock as a new Tab?"
            conditional = QMessageBox.question(
                self, "Undocked Tab", msg, QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No) == QMessageBox.Yes
            if conditional:
                index_plus_1 = self.count() + 1
                self.insertTab(index_plus_1, widget_from_tab,
                               dialog.windowIcon(), dialog.windowTitle())
                self.setTabToolTip(index_plus_1, dialog.toolTip())
                self.setTabWhatsThis(index_plus_1, dialog.whatsThis())
                return event.accept()
            else:
                return event.ignore()

        dialog.closeEvent = closeEvent_override
        self.removeTab(index)
        widget_from_tab.setParent(self.parent if self.parent else dialog)
        dialog_layout.addWidget(widget_from_tab)
        dialog.setLayout(dialog_layout)
        widget_from_tab.show()
        dialog.show()  # exec_() for modal dialog, show() for non-modal dialog
        dialog.move(QCursor.pos())

    def make_tabs_previews(self, index):
        """Make Tabs Previews for all tabs except current, if > 3 Tabs."""
        if self.count() < 4 or not self.tabBar().tab_previews:
            return False  # At least 4Tabs to use preview,and should be Enabled
        if self.timer.isActive():  # Be Race Condition Safe
            self.timer.stop()
        for old_widget in self.previews:
            old_widget.close()  # Visually Hide the Previews closing it
            old_widget.setParent(None)  # Orphan the old previews
            old_widget.destroy()  # Destroy to Free Resources
        self.previews = [QLabel(self) for i in range(self.count())]  # New Ones
        y_pos = self.size().height() - self.tabBar().tabRect(0).size().height()
        for i, widget in enumerate(self.previews):  # Iterate,set QPixmaps,Show
            if i != index:  # Dont make a pointless preview for the current Tab
                widget.setScaledContents(True)  # Auto-Scale QPixmap contents
                tabwidth = self.tabBar().tabRect(i).size().width()
                tabwidth = 200 if tabwidth > 200 else tabwidth  # Limit sizes
                widget.setPixmap(self.widget(i).grab().scaledToWidth(tabwidth))
                widget.resize(tabwidth - 1, tabwidth)
                if self.tabPosition():  # Move based on Top / Bottom positions
                    widget.move(self.tabBar().tabRect(i).left() * 1.1,
                                y_pos - tabwidth - 3)
                else:
                    widget.move(self.tabBar().tabRect(i).bottomLeft() * 1.1)
                widget.show()
        self.timer.start(1000)  # how many time display the previews
        return True
