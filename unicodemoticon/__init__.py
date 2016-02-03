#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# metadata
"""UnicodEmoticons."""

__version__ = '2.1.0'
__license__ = ' GPLv3+ LGPLv3+ '
__author__ = ' Juan Carlos '
__email__ = ' juancarlospaco@gmail.com '
__url__ = 'https://github.com/juancarlospaco/unicodemoticon'
__source__ = ('https://raw.githubusercontent.com/juancarlospaco/'
              'unicodemoticon/master/unicodemoticon.py')


import codecs
import os
import re
import logging as log

from base64 import b64encode, urlsafe_b64encode
from json import loads
from locale import getdefaultlocale
from urllib import parse, request

from html import entities
from webbrowser import open_new_tab

import unicodedata

from PyQt5.QtCore import QEvent, Qt, QTimeLine, QTimer
from PyQt5.QtGui import QCursor, QIcon, QPainter
from PyQt5.QtWidgets import (QApplication, QComboBox, QDesktopWidget, QDialog,
                             QGridLayout, QGroupBox, QHBoxLayout, QInputDialog,
                             QLabel, QLineEdit, QMainWindow, QMenu,
                             QMessageBox, QPushButton, QScrollArea,
                             QSystemTrayIcon, QTabBar, QTabWidget, QToolButton,
                             QVBoxLayout, QWidget)

from .data import CODES, STD_ICON_NAMES, UNICODEMOTICONS, AUTOSTART_DESKTOP_FILE
from .stealth_strings import string_to_stealth
from .utils import (about_python, about_self, view_code, report_bug,
                    check_for_updates, get_or_set_config_folder,
                    add_desktop_files)


def tinyslation(s: str, to: str=getdefaultlocale()[0][:2], fm="en") -> str:
    """Translate from internet via API from mymemory.translated.net,legally."""
    api = "https://mymemory.translated.net/api/get?q={st}&langpair={fm}|{to}"
    req = request.Request(url=api.format(st=parse.quote(s), fm=fm, to=to),
                          headers={'User-Agent': '', 'DNT': 1})  # DoNotTrack
    try:
        responze = request.urlopen(req, timeout=3).read().decode("utf-8")
        return loads(responze)['responseData']['translatedText']
    except:
        return str(s).strip()


##############################################################################


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


class TabWidget(QTabWidget):

    """Custom tab widget."""

    def __init__(self, parent=None, *args, **kwargs):
        """Init class custom tab widget."""
        super(TabWidget, self).__init__(parent=None, *args, **kwargs)
        self.parent, self.previews, self.timer = parent, [], QTimer(self)
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
        self.setTabBar(TabBar(self))
        self.setMovable(False)
        self.setTabsClosable(False)
        self.setTabShape(QTabWidget.Triangular)
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
        self.menu_tool.addAction("Search Unicode", self.make_search_unicode)
        self.menu_tool.addAction("Alternate Case Clipboard",
                                 self.alternate_clipboard)
        self.menu_tool.addSeparator()
        self.menu_tool.addAction(
            "Set UI Style",
            lambda: open_new_tab(os.path.join(get_or_set_config_folder(
                "unicodemoticon"), "unicodemoticon.css")))
        self.menu_tool.addAction("AutoCenter Window", self.center)
        self.menu_tool.addAction("Set Icon", self.set_icon)
        self.menu_tool.addAction(
            "Add Launcher to Desktop", lambda:  # force recreate desktop file
            add_desktop_files("unicodemoticon", AUTOSTART_DESKTOP_FILE))
        self.menu_tool.addAction("Move to Mouse position",
                                 self.move_to_mouse_position)
        self.menu_tool.addSeparator()
        self.menu_tool.addAction("Minimize", self.showMinimized)
        self.menu_tool.addAction("Hide", self.hide)
        self.menu_tool.addAction("Quit", exit)
        self.menu_help.addAction("About Python 3", about_python)
        self.menu_help.addAction("About Qt 5",
                                 lambda: QMessageBox.aboutQt(None))
        self.menu_help.addAction(
            "About Stealth Strings", lambda: open_new_tab(
                "http://gist.github.com/juancarlospaco/cc23a3919df41076252a"))
        self.menu_help.addAction("About " + __doc__, about_self)
        self.menu_help.addSeparator()
        self.menu_help.addAction("View Source Code", view_code)
        self.menu_help.addSeparator()
        self.menu_help.addAction("Report Bugs", report_bug)
        self.menu_help.addAction(
            "Check for Updates", lambda:
            QMessageBox.information(self, __doc__, check_for_updates()))
        self.setCornerWidget(self.menu_1, 1)
        self.setCornerWidget(self.menu_0, 0)
        self.currentChanged.connect(self.make_tabs_previews)
        self.currentChanged.connect(self.make_tabs_fade)
        self.tray, layout = QSystemTrayIcon(self), QVBoxLayout()
        self.menu = QMenu(__doc__)
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
        self.menu.addAction("Show", self.showMaximized)
        self.menu.addAction("Minimize", self.showMinimized)
        self.menu.addAction("AutoCenter Window", self.center)
        self.menu.addAction("To mouse position", self.move_to_mouse_position)
        self.tray.setContextMenu(self.menu)
        area, group = QScrollArea(), QGroupBox("Quick and Dirty Text Hacks !")
        area.setWidgetResizable(True)
        area.setHorizontalScrollBarPolicy(1)
        area.setWidget(group)
        group.setLayout(layout)
        self.inputx, self.alt, self.b64 = QLineEdit(), QLineEdit(), QLineEdit()
        self.b64unsafe, self.rot13 = QLineEdit(), QLineEdit()
        self.urlenc, self.urlencp = QLineEdit(), QLineEdit()
        self.snake, self.spine, self.st = QLineEdit(), QLineEdit(), QLineEdit()
        self.asci, self.camel, self.swp = QLineEdit(), QLineEdit(), QLineEdit()
        self.tran, self.fr, self.to = QLineEdit(), QComboBox(), QComboBox()
        self.container, loca = QWidget(), str(getdefaultlocale()[0][:2])
        self.fr.addItems(CODES)
        self.to.addItems(CODES)
        self.fr.setCurrentIndex(self.fr.findText(loca))
        self.to.setCurrentIndex(self.fr.findText(loca))
        layou = QHBoxLayout(self.container)
        layou.addWidget(self.tran)
        layou.addWidget(QLabel("<b>From"))
        layou.addWidget(self.fr)
        layou.addWidget(QLabel("<b>To"))
        layou.addWidget(self.to)
        self.inputx.setPlaceholderText(" Type something cool here . . .")
        self.inputx.setFocus()
        self.runtools = QPushButton("Go !", self, clicked=self.runtool)
        layout.addWidget(QLabel("<h1>Type or Paste text"))
        layout.addWidget(self.inputx)
        layout.addWidget(self.runtools)
        layout.addWidget(QLabel("Translated Text"))
        layout.addWidget(self.container)
        layout.addWidget(QLabel("Alternate case"))
        layout.addWidget(self.alt)
        layout.addWidget(QLabel("Stealth String"))
        layout.addWidget(self.st)
        layout.addWidget(QLabel("Swap case"))
        layout.addWidget(self.swp)
        layout.addWidget(QLabel("Base 64 URL Safe, for the Web"))
        layout.addWidget(self.b64)
        layout.addWidget(QLabel("Base 64"))
        layout.addWidget(self.b64unsafe)
        layout.addWidget(QLabel("ROT-13"))
        layout.addWidget(self.rot13)
        layout.addWidget(QLabel("URL Encode Plus+"))
        layout.addWidget(self.urlencp)
        layout.addWidget(QLabel("URL Encode"))
        layout.addWidget(self.urlenc)
        layout.addWidget(QLabel("Camel Case"))
        layout.addWidget(self.camel)
        layout.addWidget(QLabel("Snake Case"))
        layout.addWidget(self.snake)
        layout.addWidget(QLabel("Spine Case"))
        layout.addWidget(self.spine)
        layout.addWidget(QLabel("Sanitized,Clean out weird characters,ASCII"))
        layout.addWidget(self.asci)
        self.addTab(area, "Tools")
        area2, group2 = QScrollArea(), QGroupBox("HTML Entities !")
        area2.setWidgetResizable(True)
        area2.setHorizontalScrollBarPolicy(1)
        area2.setWidget(group2)
        added_html_entities, row, layout2, index = [], 0, QGridLayout(), 0
        l = "".join([_ for _ in UNICODEMOTICONS.values()
                     if isinstance(_, str)])
        for html_char in tuple(sorted(entities.html5.items())):
            if html_char[1] in l:
                added_html_entities.append(
                    html_char[0].lower().replace(";", ""))
                if not html_char[0].lower() in added_html_entities:
                    button = QPushButton(html_char[1], self)
                    button.released.connect(self.hide)
                    button.pressed.connect(lambda ch=html_char:
                                           self.make_preview(str(ch)))
                    button.clicked.connect(
                        lambda _, ch=html_char[0]:
                            QApplication.clipboard().setText(
                                "&{html_entity}".format(html_entity=ch)))
                    button.setToolTip("<center><h1>{0}<br>{1}".format(
                        html_char[1], self.get_description(html_char[1])))
                    button.setFlat(True)
                    font = button.font()
                    font.setPixelSize(50)
                    button.setFont(font)
                    index = index + 1  # cant use enumerate()
                    row = row + 1 if not index % 8 else row
                    layout2.addWidget(button, row, index % 8)
        group2.setLayout(layout2)
        self.addTab(area2, "HTML")
        self.widgets_to_tabs(self.json_to_widgets(UNICODEMOTICONS))
        self.set_or_get_stylesheet()
        self.make_trayicon()
        self.setMinimumSize(QDesktopWidget().screenGeometry().width() // 1.5,
                            QDesktopWidget().screenGeometry().height() // 1.5)
        # self.showMaximized()

    def build_submenu(self, char_list: (str, tuple), submenu: QMenu) -> QMenu:
        """Take a list of characters and a submenu and build actions on it."""
        submenu.setProperty("emoji_menu", True)
        submenu.setWindowOpacity(0.9)
        submenu.setToolTipsVisible(True)
        for _char in sorted(char_list):
            action = submenu.addAction(_char.strip())
            action.setToolTip(self.get_description(_char))
            action.hovered.connect(lambda char=_char: self.make_preview(char))
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

    def runtool(self, *args):
        """Run all text transformation tools."""
        txt = str(self.inputx.text())
        if not len(txt.strip()):
            return
        for field in (
            self.alt, self.b64, self.b64unsafe, self.rot13, self.urlenc,
            self.urlencp, self.snake, self.spine, self.asci, self.camel,
                self.swp, self.tran, self.st):
            field.clear()
            field.setReadOnly(True)
        self.alt.setText(self.make_alternate_case(txt))
        self.swp.setText(txt.swapcase())
        self.b64.setText(urlsafe_b64encode(
            bytes(txt, "utf-8")).decode("utf-8"))
        self.b64unsafe.setText(b64encode(bytes(txt, "utf-8")).decode("utf-8"))
        self.rot13.setText(codecs.encode(txt, "rot-13"))
        self.urlencp.setText(parse.quote_plus(txt, encoding="utf-8"))
        self.urlenc.setText(parse.quote(txt, encoding="utf-8"))
        self.camel.setText(txt.title().replace(" ", ""))
        self.snake.setText(txt.replace(" ", "_"))
        self.spine.setText(txt.replace(" ", "-"))
        self.asci.setText(re.sub(r"[^\x00-\x7F]+", "", txt))
        self.st.setText(string_to_stealth(txt))
        if self.fr.currentText() != self.to.currentText() and len(txt) < 999:
            self.tran.setText(tinyslation(txt.strip().replace("\n", " "),
                              str(self.to.currentText()),
                              str(self.fr.currentText())))

    def make_search_unicode(self):
        """Make a Pop-Up Dialog to search Unicode Emoticons."""
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

    def set_or_get_stylesheet(self, stylesheet: str="") -> str:
        """Add a default stylesheet if needed."""
        style_file = os.path.join(
            get_or_set_config_folder("unicodemoticon"), "unicodemoticon.css")
        log.info("To Customize the Look'n'Feel Edit the file: " + style_file)
        if not os.path.isfile(style_file):
            log.info("Writing Default CSS StyleSheet file: " + style_file)
            with open(style_file, "w", encoding="utf-8") as style_file_object:
                style_file_object.write("/* Write your Custom Style here */\n")
        log.debug("Reading CSS StyleSheet file: " + style_file)
        with open(style_file, "r", encoding="utf-8") as style_file_object:
            stylesheet = style_file_object.read().strip()
        return stylesheet

    def make_preview(self, emoticon_text: str):
        """Make Emoticon Previews for the current Hovered one."""
        log.debug(emoticon_text)
        if self.taimer.isActive():  # Be Race Condition Safe
            self.taimer.stop()
        self.preview.setText("  " + emoticon_text + "  ")
        self.preview.move(QCursor.pos())
        self.preview.show()
        self.taimer.start(1000)  # how many time display the previews

    def json_to_widgets(self, jotason: dict):
        """Take a json string object return QWidgets."""
        dict_of_widgets, row = {}, 0
        for titlemotes in tuple(sorted(jotason.items())):
            layout, tit = QGridLayout(), str(titlemotes[0]).strip()[:9].title()
            grid_cols = 2 if tit.lower() == "multichar" else 8
            for index, emote in enumerate(tuple(set(sorted(titlemotes[1])))):
                button = QPushButton(emote, self)
                button.clicked.connect(lambda _, c=emote:
                                       QApplication.clipboard().setText(c))
                button.released.connect(self.hide)
                button.pressed.connect(lambda c=emote: self.make_preview(c))
                button.setToolTip("<center><h1>{0}<br>{1}".format(
                    emote, self.get_description(emote)))
                button.setFlat(True)
                font = button.font()
                font.setPixelSize(50)
                button.setFont(font)
                row = row + 1 if not index % grid_cols else row
                layout.addWidget(button, row, index % grid_cols)
            area, group = QScrollArea(), QGroupBox(tit + " !")
            area.setWidgetResizable(True)
            area.setHorizontalScrollBarPolicy(1)
            area.setWidget(group)
            group.setLayout(layout)
            dict_of_widgets.update({tit: area})
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
            icon = QInputDialog.getItem(None, __doc__, "<b>Choose Icon name?:",
                                        STD_ICON_NAMES, 0, False)[0]
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
