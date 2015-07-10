#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# metadata
"""UnicodEmoticons."""
__version__ = '1.2.0'
__license__ = ' GPLv3+ LGPLv3+ '
__author__ = ' Juan Carlos '
__email__ = ' juancarlospaco@gmail.com '
__url__ = 'https://github.com/juancarlospaco/unicodemoticon'
__source__ = ('https://raw.githubusercontent.com/juancarlospaco/'
              'unicodemoticon/master/unicodemoticon.py')


# imports
import functools
import logging as log
import os
import signal
import sys
import time
import socket
import unicodedata
from copy import copy
from ctypes import byref, cdll, create_string_buffer
from datetime import datetime
from getopt import getopt
from os import path
from platform import platform, python_version
from subprocess import call
from tempfile import gettempdir
from urllib import request
from webbrowser import open_new_tab
from random import randint

from html import entities

from PyQt5.QtCore import QUrl, QTimer, Qt

from PyQt5.QtGui import QCursor, QFont, QIcon, QPalette, QPainter, QPen, QColor

from PyQt5.QtNetwork import (QNetworkAccessManager, QNetworkProxyFactory,
                             QNetworkRequest)

from PyQt5.QtWidgets import (QAction, QApplication, QInputDialog, QMenu,
                             QMessageBox, QProgressDialog, QStyle, QLabel,
                             QSystemTrayIcon)

try:
    import resource  # windows dont have resource
except ImportError:
    resource = None


QSS_STYLE = """QWidget:disabled { color: lightgray; font-weight: bold }
QWidget { background-color: #302F2F; border-radius: 9px; font-family: Oxygen }
QMenu[emoji_menu] { border: 0; color: silver; background-color: transparent }
QMenu[emoji_menu]::item { padding: 1px 1em 1px 1em; margin: 0; border: 0 }
QMenu[emoji_menu]::item:selected { background-color: skyblue; color: black }
QMenu[emoji_menu]::item:disabled { background-color: transparent }"""

AUTOSTART_DESKTOP_FILE = """[Desktop Entry]
Comment=Trayicon with Unicode Emoticons.
Exec=chrt --idle 0 unicodemoticon.py
GenericName=Trayicon with Unicode Emoticons.
Icon=system-run
Name=UnicodEmoticon
StartupNotify=false
Terminal=false
Type=Application
Categories=Utility
X-DBUS-ServiceName=unicodemoticon
X-DBUS-StartupType=none
X-KDE-StartupNotify=false
X-KDE-SubstituteUID=false"""

STD_ICON_NAMES = tuple(sorted(set("""emblem-default emblem-documents start-here
emblem-downloads emblem-favorite emblem-important emblem-mail emblem-photos
emblem-readonly emblem-shared emblem-symbolic-link emblem-synchronized
emblem-system emblem-unreadable face-angel face-angry face-crying face-devilish
face-embarrassed face-cool face-kiss face-laugh face-monkey face-plain
face-raspberry face-sad face-sick face-smile face-smile-big face-smirk
face-surprise face-tired face-uncertain face-wink face-worried go-home
insert-image insert-link insert-object insert-text list-add edit-copy
edit-find-replace edit-paste tools-check-spelling accessories-character-map
accessories-dictionary accessories-text-editor preferences-desktop-font
preferences-desktop-keyboard applications-other applications-utilities
preferences-other user-bookmarks application-x-executable image-missing
""".strip().lower().replace("\n", " ").split(" "))))  # use your themes icons

HTMLS = ("©®€℅№∗√∞≋≡≢⊕⊖⊗⊛☆★⏧⌖☎♀♂✓✗⦿⧉⩸*¢£¥×¤ж—†•π℗Ω≬⊹✠⩐∰§´»«@θ¯⋄∇♥✗"
         "¼½¾⅓⅔⅕⅖⅗⅘⅙⅚⅛⅜⅝⅞²³𝒜𝒞𝒟𝒢𝒥𝒦𝒩𝒪𝒫𝒬𝒮𝒯𝒰𝒱𝒲𝒳𝒴𝒵𝔅𝔇𝔉𝔐ℵαβγδελμψ^@⋙⋘™✔♫")

UNICODEMOTICONS = {
    "sex":
        "♀♂⚢⚣⚤⚥⚧☿👭👬👫",

    "cats":
        "😸😹😺😻😼😽😾😿🙀",

    "funny":
        "😀😁😂😃😅😆😇😈😉😊😋😌😍😎😏😗😘😙😚😛😜😝☺☻👿👀",

    "sad":
        "😐😒😓😔😕😖😤😞😟😠😡😢😣😥😦😧😨😩😪😫😭😮😯😰😱😲😳😴😵☹😷",

    "music":
        ("♫♪♭♩🎶🎵🎼", "🎨🎬🎤🎧🎹", "🎻🎺🎷🎸"),

    "arrows":
        "⇉⇇⇈⇊➺⇦⇨⇧⇩↔↕↖↗↘↙↯↰↱↲↳↴↵↶↷↺↻➭🔄⏪⏩⏫⏬",

    "alphanumeric":
        ("①②③④⑤⑥⑦⑧⑨⑩", "➊➋➌➍➎➏➐➑➒➓", "½¾∞", "⒈⒉⒊⒋⒌⒍⒎⒏⒐⒑",
         "ⓐⓑⓒⓓⓔⓕⓖⓗⓘⓙⓚⓛⓜⓝⓞⓟⓠⓡⓢⓣⓤⓥⓦⓨⓩ"),

    "symbols":
        "‼⁉…❓✔✗☑☒➖➗❌™®©Ω℮₤₧❎✅➿♿☠☯☮☘💲💯🚭🚮💤㋡🔞🚼🛀🚬🚭🌀﻿",

    "stars":
        "✵✪✬✫✻✴☆✨✶✩★✾❄❀✿🃏⚝⚹⚜🌟🌠💫💥",

    "hearts":
        "♥♡❤❦☙❣💌💘💞💖💓💗💟💝💑🌹💋💔💕",

    "hands":
        "✌☜☞☝☟✋✊✍👊👌👏🙌👍👎",

    "weather":
        "⛅⛈☀☁⚡☔☂❄☃☽☾🌞🌊🌋🌌🌁",

    "clothes":
        "🎩👑👒👟👞👡👠👢👕👔👚👗🎽👖👘👙💼👜👝👛👓🎀🌂💄",

    "plants":
        "💐🌸🌷🍀🌹🌻🌺🍁🍃🍂🌿🌾🍄🌵🌴🌲🌳🌰🌱🌼",

    "geometry":
        "■●▲▼▓▒░◑◐〇◈▣▨▧▩◎◊□◕☉",

    "zodiac and chess":
        "♈♉♊♋♌♍♎♏♐♑♒♓♔♕♖♗♘♙♚♛♜♝♞♟",

    "recycle":
        "♲♻♳♴♵♶♷♸♹♺♼♽♾",

    "religion":
        "☦☧☨☩☪☫☬☭☯࿊࿕☥✟✠✡⛤",

    "animals faces":
        "🐭🐮🐵🐯🐰🐲🐳🐴🐶🐷🐸🐹🐺🐻🐼",

    "animals":
        "🐞🐝🐜🐛🐀🐁🐂🐃🐄🐅🐆🐇🐈🐉🐊🐋🐌🐍🐎🐏🐐🐑",

    "animals 2":
        "🐒🐓🐔🐕🐖🐗🐘🐪🐫🐩🐧🐨🐙🐬🐚🐟🐠🐡🐢🐣🐤🐥🐦",

    "faces":
        "👲👳👮👷💂👶👦👧👨👩👴👵👱👼👸👹👺🙈🙉🙊💀👽👯💇",

    "sports":
        "👾🎮🎴🀄🎲🎯🏈🏀⚽⚾🎾🎱🏉🎳⛳🚵🚴🏁🏇🏆🎿🏂🏊🏄⚾🎣",

    "fruits":
        "🍎🍏🍊🍋🍒🍇🍉🍓🍑🍈🍌🍐🍍🍠🍆🍅🌽",

    "food":
        "☕🍵🍶🍼🍺🍻🍸🍹🍷🍴🍕🍔🍟🍗🍖🍝🍛🍤🍱🍣🍥🍙🍜🍲🍢🍡🍳🍞🍩🍮🍦🍨🍧🎂🍰🍪🍫🍬🍭🍯",

    "buildings":
        "🏠🏡🏫🏢🏣🏥🏪🏩🏨💒⛪🏬🏤🌇🌆🏯🏰⛺🏭🗼🗻🌄🌅🌃🗽🌉🎠🎡⛲🎢🚢🗽",

    "objects":
        "🎍🎎🎒🎓🎏🎃👻🎅🎄🎁🎋🎉🎊🎈🎌🌎💩⚙⚖⚔⚒🔐🔗🔩",

    "tech":
        "🎥📷📹📼💿📀💽💾💻📱☎📞📟📠📡📺📻🔊🔉🔇🔔🔕📢⏰🔓🔒🔑💡🔌🔍🔧🔨📲⚛⌛⏳⏰⌚✂ℹ☢☣☤✇✆",

    "transport":
        "⛵🚤🚣⚓🚀✈💺🚁🚂🚊🚆🚈🚇🚋🚎🚌🚍🚙🚕🚖🚛🚚🚓🚔🚒🚑🚐🚲🚡🚟🚜",

    "papers":
        "📧✉📩📨📫📪📬📭📮📝📃📑📊📋📆📁📂✂📌📎📏📐📗📓📔📒📚📖🔖📛🔬🔭📰",

    "multi-character":
        ("d-( ʘ‿ʘ )_m", "ಠ_ಠ", "ಢ_ಢ", "┌П┐(⌣د̲⌣)┌П┐", "(￣(工)￣)", "⊙_ʘ",
         "ಡ_ಡ", "⊙﹏⊙", "⊙▃⊙", "¯\_(ツ)_/¯", "(づ｡◕‿‿◕｡)づ", "⊂(ʘ‿ʘ)つ",
         "ლ(ಠ_ಠ ლ)", "≖_≖", "⊂(`･ω･´)つ", "Ծ_Ծ", "¯＼(⊙_ʘ)/¯", "ʕ•ᴥ•ʔ",
         "͡° ͜ʖ﻿ ͡°", "ᕦ(ò_óˇ)ᕤ", "(¬▂¬)", "█▄▄ ███ █▄▄", "(⌐■_■)",
         "✌.|•͡˘‿•͡˘|.✌", "[̲̅$̲̅(̲̅ιοο̲̅)̲̅$̲̅]", "(｡◕‿‿◕｡)", "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧",
         "٩(｡͡•‿•｡)۶", "∩(︶▽︶)∩", "☜(ﾟヮﾟ☜)", "Ƹ̵̡Ӝ̵̨̄Ʒ", "┐(;´༎ຶД༎ຶ`)┌",
         "(✿つ°ヮ°)つ  └⋃┘", "(つ°ヮ°)つ  （。Y。）", "(✿ ◕‿◕) ᓄ✂╰⋃╯",
         "(つ°ヮ°)つ  (‿|‿)",  "▄︻̷̿┻̿═━一", "(｡♥‿‿♥｡)", "╭∩╮（︶︿︶）╭∩╮",
         "<('()))}><{", "┐(´～`；)┌", "(╯°□°）╯︵ ┻━┻", "(ง'̀-'́)ง", "ᕙ(⇀‸↼‶)ᕗ"),

    "multi-character 2":
        ("ლ(=ↀωↀ=)ლ", "ヾ(*ΦωΦ)ﾉ", "m_༼ ༎ຶ ෴ ༎ຶ༽_m", "\(•⊙ω⊙•)/",
         "o(╥﹏╥)o",
         "(－‸ლ)", "(͠≖ ͜ʖ͠≖)", "╭∩╮( ͡⚆ ͜ʖ ͡⚆)╭∩╮", "ლ(╹◡╹ლ)", "(๑˃̵ᴗ˂̵)و",
         "(V) (°,,,°) (V)", "( ͠° ͟ʖ ͡°)", "ಠ_ರೃ", "🌀_🌀", "♥‿♥",
         "₍₍ ᕕ( ･᷄ὢ･᷅ )ᕗ⁾⁾",  "*｡٩(ˊωˋ*)و✧*｡",  "(•ิ_•ิ)?",
         "(　-̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥᷄◞ω◟-̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥᷅ )",
         "(つ°ヮ°)つ  (≬)", "┻━┻ ︵ \(°□°)/ ︵ ┻━┻",
         "¸.·´¯`·.´¯`·.¸¸.·´¯`·.¸><(((º>", "ᶠᶸᶜᵏ♥ᵧₒᵤ", "\,,/(◣_◢)\,,/",
         "(⌐■_■)--︻╦╤─ - - - (╥﹏╥)", "\m/_(>_<)_\m/", "Yᵒᵘ Oᶰˡʸ Lᶤᵛᵉ Oᶰᶜᵉ",
         "(つ -‘ _ ‘- )つ", "^⨀ᴥ⨀^", "ლ(́◕◞Ѿ◟◕‵ლ)", "┌∩┐(⋟﹏⋞)┌∩┐",
         "ˁ˚ᴥ˚ˀ", "ヽ(￣(ｴ)￣)ﾉ", "(⋟﹏⋞)", "⊂(✰‿✰)つ",
         "(づ ￣ ³￣)づ ⓈⓂⓄⓄⓉⒽ", "❚█══█❚ ▐━━━━━▌")
}


###############################################################################


def typecheck(f):
    """Decorator for Python3 annotations to type-check inputs and outputs."""
    def __check_annotations(tipe):
        _type, is_ok = None, isinstance(tipe, (type, tuple, type(None)))
        if is_ok:  # Annotations can be Type or Tuple or None
            _type = tipe if isinstance(tipe, tuple) else tuple((tipe, ))
            if None in _type:  # if None on tuple replace with type(None)
                _type = tuple([_ if _ is not None else type(_) for _ in _type])
        return _type, is_ok

    @functools.wraps(f)  # wrap a function or method to Type Check it.
    def decorated(*args, **kwargs):
        msg = "Type check error: {0} must be {1} but is {2} on function {3}()."
        notations, f_name = tuple(f.__annotations__.keys()), f.__code__.co_name
        for i, name in enumerate(f.__code__.co_varnames):
            if name not in notations:
                continue  # this arg name has no annotation then skip it.
            _type, is_ok = __check_annotations(f.__annotations__.get(name))
            if is_ok:  # Force to tuple
                if i < len(args) and not isinstance(args[i], _type):
                    log.critical(msg.format(repr(args[i])[:50], _type,
                                            type(args[i]), f_name))
                elif name in kwargs and not isinstance(kwargs[name], _type):
                    log.critical(msg.format(repr(kwargs[name])[:50], _type,
                                            type(kwargs[name]), f_name))
        out = f(*args, **kwargs)
        _type, is_ok = __check_annotations(f.__annotations__.get("return"))
        if is_ok and not isinstance(out, _type) and "return" in notations:
            log.critical(msg.format(repr(out)[:50], _type, type(out), f_name))
        return out    # The output result of function or method.
    return decorated  # The decorated function or method.


class Downloader(QProgressDialog):

    """Downloader Dialog with complete informations and progress bar."""

    def __init__(self, parent=None):
        """Init class."""
        super(Downloader, self).__init__(parent)
        self.setWindowTitle(__doc__)
        if not os.path.isfile(__file__) or not __source__:
            return
        if not os.access(__file__, os.W_OK):
            error_msg = ("Destination file permission denied (not Writable)! "
                         "Try again to Update but as root or administrator.")
            log.critical(error_msg)
            QMessageBox.warning(self, __doc__.title(), error_msg)
            return
        self._time, self._date = time.time(), datetime.now().isoformat()[:-7]
        self._url, self._dst = __source__, __file__
        log.debug("Downloading from {} to {}.".format(self._url, self._dst))
        if not self._url.lower().startswith("https:"):
            log.warning("Unsecure Download over plain text without SSL.")
        self.template = """<h3>Downloading</h3><hr><table>
        <tr><td><b>From:</b></td>      <td>{}</td>
        <tr><td><b>To:  </b></td>      <td>{}</td> <tr>
        <tr><td><b>Started:</b></td>   <td>{}</td>
        <tr><td><b>Actual:</b></td>    <td>{}</td> <tr>
        <tr><td><b>Elapsed:</b></td>   <td>{}</td>
        <tr><td><b>Remaining:</b></td> <td>{}</td> <tr>
        <tr><td><b>Received:</b></td>  <td>{} MegaBytes</td>
        <tr><td><b>Total:</b></td>     <td>{} MegaBytes</td> <tr>
        <tr><td><b>Speed:</b></td>     <td>{}</td>
        <tr><td><b>Percent:</b></td>     <td>{}%</td></table><hr>"""
        self.manager = QNetworkAccessManager(self)
        self.manager.finished.connect(self.save_downloaded_data)
        self.manager.sslErrors.connect(self.download_failed)
        self.progreso = self.manager.get(QNetworkRequest(QUrl(self._url)))
        self.progreso.downloadProgress.connect(self.update_download_progress)
        self.show()
        self.exec_()

    def save_downloaded_data(self, data):
        """Save all downloaded data to the disk and quit."""
        log.debug("Download done. Update Done.")
        with open(os.path.join(self._dst), "wb") as output_file:
            output_file.write(data.readAll())
        data.close()
        QMessageBox.information(self, __doc__.title(),
                                "<b>You got the latest version of this App!")
        del self.manager, data
        return self.close()

    def download_failed(self, download_error):
        """Handle a download error, probable SSL errors."""
        log.error(download_error)
        QMessageBox.warning(self, __doc__.title(), str(download_error))

    def seconds_time_to_human_string(self, time_on_seconds=0):
        """Calculate time, with precision from seconds to days."""
        minutes, seconds = divmod(int(time_on_seconds), 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)
        human_time_string = ""
        if days:
            human_time_string += "%02d Days " % days
        if hours:
            human_time_string += "%02d Hours " % hours
        if minutes:
            human_time_string += "%02d Minutes " % minutes
        human_time_string += "%02d Seconds" % seconds
        return human_time_string

    def update_download_progress(self, bytesReceived, bytesTotal):
        """Calculate statistics and update the UI with them."""
        downloaded_MB = round(((bytesReceived / 1024) / 1024), 2)
        total_data_MB = round(((bytesTotal / 1024) / 1024), 2)
        downloaded_KB, total_data_KB = bytesReceived / 1024, bytesTotal / 1024
        # Calculate download speed values, with precision from Kb/s to Gb/s
        elapsed = time.clock()
        if elapsed > 0:
            speed = round((downloaded_KB / elapsed), 2)
            if speed > 1024000:  # Gigabyte speeds
                download_speed = "{} GigaByte/Second".format(speed // 1024000)
            if speed > 1024:  # MegaByte speeds
                download_speed = "{} MegaBytes/Second".format(speed // 1024)
            else:  # KiloByte speeds
                download_speed = "{} KiloBytes/Second".format(int(speed))
        if speed > 0:
            missing = abs((total_data_KB - downloaded_KB) // speed)
        percentage = int(100.0 * bytesReceived // bytesTotal)
        self.setLabelText(self.template.format(
            self._url.lower()[:99], self._dst.lower()[:99],
            self._date, datetime.now().isoformat()[:-7],
            self.seconds_time_to_human_string(time.time() - self._time),
            self.seconds_time_to_human_string(missing),
            downloaded_MB, total_data_MB, download_speed, percentage))
        self.setValue(percentage)


###############################################################################


class Menu(QMenu):

    """Custom QMenu widget."""

    def __init__(self, parent=None, *args, **kwargs):
        """Init class custom tab widget."""
        super(Menu, self).__init__(parent=None, *args, **kwargs)
        self.setWindowOpacity(0.8)
        self.setAttribute(Qt.WA_OpaquePaintEvent, False)  # no opaque paint
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # translucent
        self.setStyleSheet("background-color:transparent")  # default style

    def paintEvent(self, event):
        """Paint transparent background,animated pattern,background text."""
        painter, font = QPainter(self), self.font()
        painter.fillRect(event.rect(), Qt.transparent)  # fill transparent rect
        painter.setPen(Qt.NoPen)  # set the pen to no pen
        painter.setBrush(QColor("black"))  # Background Color
        painter.setOpacity(0.85)  # Background Opacity
        painter.drawRoundedRect(self.rect(), 40, 40)  # Back Rounded Borders
        for i in range(512):  # animated random dots background pattern
            x = randint(10, self.size().width() - 10)
            y = randint(10, self.size().height() - 10)
            painter.setPen(QPen(QColor(randint(9, 255), randint(9, 255), 255)))
            painter.drawPoint(x, y)
        QMenu.paintEvent(self, event)


class MainWindow(QSystemTrayIcon):

    """Main widget for UnicodEmoticons,not really a window since not needed."""

    def __init__(self, icon, parent=None):
        """Tray icon main widget."""
        super(MainWindow, self).__init__(icon, parent)
        log.debug("Starting {}.".format(__doc__))
        self.setIcon(icon)
        self.setToolTip(__doc__ + "\nPick 1 Emoticon, use CTRL+V to Paste it!")
        self.traymenu = Menu("Emoticons")
        self.traymenu.addAction("    Emoticons").setDisabled(True)
        self.traymenu.setIcon(icon)
        self.traymenu.addSeparator()
        self.traymenu.setProperty("emoji_menu", True)
        self.activated.connect(self.click_trap)
        self.timer, self.preview = QTimer(self), QLabel("Preview")
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(lambda: self.preview.hide())
        font = self.preview.font()
        font.setPixelSize(100)
        self.preview.setFont(font)
        self.preview.setDisabled(True)
        self.preview.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.preview.setAttribute(Qt.WA_TranslucentBackground, True)
        list_of_labels = sorted(UNICODEMOTICONS.keys())  # menus
        menus = [self.traymenu.addMenu(lbl.title()) for lbl in list_of_labels]
        self.traymenu.addSeparator()
        menu_html = self.traymenu.addMenu("HTML5 Code")
        menu_html.setProperty("emoji_menu", True)
        menu_html.setWindowOpacity(0.9)
        log.debug("Building Emoticons SubMenus.")
        for item, label in zip(menus, list_of_labels):
            item.setStyleSheet("padding:0;margin:0;border:0;menu-scrollable:1")
            font = item.font()
            font.setPixelSize(18)
            item.setFont(font)
            self.build_submenu(UNICODEMOTICONS[label], item)
        # html entities
        added_html_entities = []
        menu_html.setStyleSheet("font-size:25px;padding:0;margin:0;border:0")
        for html_char in tuple(sorted(entities.html5.items())):
            if html_char[1] in HTMLS:
                added_html_entities.append(
                    html_char[0].lower().replace(";", ""))
                if not html_char[0].lower() in added_html_entities:
                    action = menu_html.addAction(html_char[1])
                    action.hovered.connect(lambda ch=html_char: log.debug(ch))
                    action.triggered.connect(
                        lambda _, ch=html_char[0]:
                            QApplication.clipboard().setText(
                                "&{html_entity}".format(html_entity=ch)))
        self.traymenu.addAction("AlTeRnAtE-CaSe", self.make_alternate_case)
        self.traymenu.addSeparator()
        # help
        helpMenu = self.traymenu.addMenu("Options...")
        helpMenu.setProperty("emoji_menu", True)
        helpMenu.setWindowOpacity(0.9)
        helpMenu.addAction("About Python 3",
                           lambda: open_new_tab('https://python.org'))
        helpMenu.addAction("About Qt 5", lambda: QMessageBox.aboutQt(None))
        helpMenu.addAction("About " + __doc__, lambda: open_new_tab(__url__))
        helpMenu.addSeparator()
        helpMenu.addAction("View Source Code", lambda: open_new_tab(__file__))
        helpMenu.addSeparator()
        helpMenu.addAction("Report Bugs", lambda:
                           open_new_tab(__url__ + '/issues?state=open'))
        helpMenu.addAction("Check for updates", lambda: Downloader())
        helpMenu.addSeparator()
        helpMenu.addAction("Set Icon", self.set_icon)
        helpMenu.addAction("Set UI Style", lambda: open_new_tab(path.join(
            self.get_or_set_config_folder("unicodemoticon"),
            "unicodemoticon.css")))
        self.traymenu.addSeparator()
        quit_action = self.traymenu.addAction("    Quit", self.close)
        quit_action.setMenuRole(QAction.QuitRole)
        self.setContextMenu(self.traymenu)
        self.show()
        self.add_desktop_files()
        custom_style_sheet = self.set_or_get_stylesheet().strip()
        self.traymenu.setStyleSheet(custom_style_sheet)
        self.preview.setStyleSheet(custom_style_sheet)
        helpMenu.setStyleSheet(custom_style_sheet)

    @typecheck
    def make_alternate_case(self) -> str:
        """Make alternating camelcase clipboard,if > 3 chars and not digits."""
        clipboard_text = str(QApplication.clipboard().text()).strip()
        funky_camelcase = "Need > 3 letters for Alternating CamelCase."
        if len(clipboard_text) > 3 and not clipboard_text.isdigit():
            funky_camelcase = "".join([_.lower() if i % 2 else _.upper()
                                       for i, _ in enumerate(clipboard_text)])
            log.debug(funky_camelcase)
            QApplication.clipboard().setText(funky_camelcase)
        else:
            log.warning(funky_camelcase)
        return funky_camelcase

    @typecheck
    def build_submenu(self, char_list: (str, tuple), submenu: QMenu) -> QMenu:
        """Take a list of characters and a submenu and build actions on it."""
        submenu.setProperty("emoji_menu", True)
        for _char in sorted(char_list):
            submenu.setWindowOpacity(0.9)
            submenu.setToolTipsVisible(True)
            action = submenu.addAction(_char.strip())
            if len(_char) == 1:
                try:
                    action.setToolTip(unicodedata.name(_char).title())
                except ValueError:
                    pass
            action.hovered.connect(lambda char=_char: self.make_preview(char))
            action.triggered.connect(
                lambda _, char=_char: QApplication.clipboard().setText(char))
        return submenu

    @typecheck
    def make_preview(self, emoticon_text: str):
        """Make Emoticon Previews for the current Hovered one."""
        log.debug(emoticon_text)
        if self.timer.isActive():  # Be Race Condition Safe
            self.timer.stop()
        self.preview.setText("  " + emoticon_text + "  ")
        self.preview.move(QCursor.pos())
        self.preview.show()
        self.timer.start(1000)  # how many time display the previews

    def click_trap(self, value):
        """Trap the mouse tight click."""
        if value == self.Trigger:  # left click
            self.traymenu.exec_(QCursor.pos())

    @typecheck
    def add_desktop_files(self):
        """Add to autostart of the Desktop."""
        autostart_file = path.join(self.get_or_set_config_folder("autostart"),
                                   "unicodemoticon.desktop")
        config_folder_exists = os.path.isdir(os.path.join(path.expanduser("~"),
                                                          ".config/autostart"))
        if config_folder_exists and not os.path.isfile(autostart_file):
            log.info("Writing Auto-Start file: " + autostart_file)
            with open(autostart_file, "w", encoding="utf-8") as start_file:
                start_file.write(AUTOSTART_DESKTOP_FILE)
        desktop_file = path.join(
            path.expanduser("~"),
            ".local/share/applications/unicodemoticon.desktop")
        apps_folder_exists = os.path.isdir(os.path.join(
            os.path.expanduser("~"), ".local/share/applications"))
        if apps_folder_exists and not os.path.isfile(desktop_file):
            log.info("Writing Desktop Launcher file: " + desktop_file)
            with open(desktop_file, "w", encoding="utf-8") as desktop_file:
                desktop_file.write(AUTOSTART_DESKTOP_FILE)

    @typecheck
    def set_or_get_stylesheet(self, stylesheet: str=QSS_STYLE) -> str:
        """Add a default stylesheet if needed."""
        style_file = path.join(self.get_or_set_config_folder("unicodemoticon"),
                               "unicodemoticon.css")
        log.info("To Customize the Look'n'Feel Edit the file: " + style_file)
        if not os.path.isfile(style_file):
            log.info("Writing Default CSS StyleSheet file: " + style_file)
            with open(style_file, "w", encoding="utf-8") as style_file_object:
                style_file_object.write(stylesheet.strip())
        log.debug("Reading CSS StyleSheet file: " + style_file)
        with open(style_file, "r", encoding="utf-8") as style_file_object:
            stylesheet = style_file_object.read().strip()
        return stylesheet

    @typecheck
    def get_or_set_config_folder(self, appname: (str, None)=None) -> str:
        """Get config folder cross-platform, try to always return a path."""
        if sys.platform.startswith("darwin"):  # Apples Macos
            config_path = os.path.expanduser("~/Library/Preferences")
        elif sys.platform.startswith("win"):  # Windown
            config_path = os.getenv("APPDATA", os.path.expanduser("~/.config"))
        else:
            config_path = os.getenv("XDG_CONFIG_HOME",
                                    os.path.expanduser("~/.config"))
        if appname and len(appname) and isinstance(appname, str):
            config_path = os.path.join(config_path, appname.strip())
        log.debug("Config folder for {} is: {}.".format(appname, config_path))
        if not os.path.isdir(config_path):
            log.debug("Creating new Config folder: {}.".format(config_path))
            os.makedirs(config_path)
        return config_path

    @typecheck
    def set_icon(self, icon: (None, str)=None) -> str:
        """Return a string with opendesktop standard icon name for Qt."""
        if not icon:
            icon = QInputDialog.getItem(None, __doc__, "<b>Choose Icon name?:",
                                        STD_ICON_NAMES, 0, False)[0]
        if icon:
            log.debug("Setting Tray Icon name to: {}.".format(icon))
            self.setIcon(QIcon.fromTheme("{}".format(icon)))
        return icon

    def close(self):
        """Overload close method."""
        log.debug("Closing.")
        return sys.exit(0)


###############################################################################


@typecheck
def make_post_execution_message(app: str=__doc__.splitlines()[0].strip()):
    """Simple Post-Execution Message with information about RAM and Time.

    >>> make_post_execution_message() >= 0
    True
    """
    ram_use = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss *
                  resource.getpagesize() / 1024 / 1024 if resource else 0)
    ram_all = int(os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
                  / 1024 / 1024)
    msg = "Total Maximum RAM Memory used: ~{0} of {1} MegaBytes.".format(
        ram_use, ram_all)
    log.info(msg)
    print("Thanks for using this App,share your experience!{0}".format("""
    Twitter: https://twitter.com/home?status=I%20Like%20{n}!:%20{u}
    Facebook: https://www.facebook.com/share.php?u={u}&t=I%20Like%20{n}
    G+: https://plus.google.com/share?url={u}""".format(u=__url__, n=app)))
    return msg


@typecheck
def make_root_check_and_encoding_debug() -> bool:
    """Debug and Log Encodings and Check for root/administrator,return Boolean.

    >>> make_root_check_and_encoding_debug()
    True
    """
    log.info(__doc__ + __version__)
    log.debug("Python {0} on {1}.".format(python_version(), platform()))
    log.debug("STDIN Encoding: {0}.".format(sys.stdin.encoding))
    log.debug("STDERR Encoding: {0}.".format(sys.stderr.encoding))
    log.debug("STDOUT Encoding:{}".format(getattr(sys.stdout, "encoding", "")))
    log.debug("Default Encoding: {0}.".format(sys.getdefaultencoding()))
    log.debug("FileSystem Encoding: {0}.".format(sys.getfilesystemencoding()))
    log.debug("PYTHONIOENCODING Encoding: {0}.".format(
        os.environ.get("PYTHONIOENCODING", None)))
    os.environ["PYTHONIOENCODING"] = "utf-8"
    if not sys.platform.startswith("win"):  # root check
        if not os.geteuid():
            log.critical("Runing as root is not Recommended,NOT Run as root!.")
            return False
    elif sys.platform.startswith("win"):  # administrator check
        if getuser().lower().startswith("admin"):
            log.critical("Runing as Administrator is not Recommended!.")
            return False
    return True


@typecheck
def set_process_name_and_cpu_priority(name: str) -> bool:
    """Set process name and cpu priority.

    >>> set_process_name_and_cpu_priority("test_test")
    True
    """
    try:
        os.nice(19)  # smooth cpu priority
        libc = cdll.LoadLibrary("libc.so.6")  # set process name
        buff = create_string_buffer(len(name.lower().strip()) + 1)
        buff.value = bytes(name.lower().strip().encode("utf-8"))
        libc.prctl(15, byref(buff), 0, 0, 0)
    except Exception:
        return False  # this may fail on windows and its normal, so be silent.
    else:
        log.debug("Process Name set to: {0}.".format(name))
        return True


@typecheck
def set_single_instance(name: str, single_instance: bool=True, port: int=8888):
    """Set process name and cpu priority, return socket.socket object or None.

    >>> isinstance(set_single_instance("test"), socket.socket)
    True
    """
    __lock = None
    if single_instance:
        try:  # Single instance app ~crossplatform, uses udp socket.
            log.info("Creating Abstract UDP Socket Lock for Single Instance.")
            __lock = socket.socket(
                socket.AF_UNIX if sys.platform.startswith("linux")
                else socket.AF_INET, socket.SOCK_STREAM)
            __lock.bind(
                "\0_{name}__lock".format(name=str(name).lower().strip())
                if sys.platform.startswith("linux") else ("127.0.0.1", port))
        except socket.error as e:
            log.warning(e)
        else:
            log.info("Socket Lock for Single Instance: {}.".format(__lock))
    else:  # if multiple instance want to touch same file bad things can happen
        log.warning("Multiple instance on same file can cause Race Condition.")
    return __lock


@typecheck
def make_logger(name: str=str(os.getpid())) -> object:
    """Build and return a Logging Logger."""
    log.basicConfig(level=-1, format="%(levelname)s:%(asctime)s %(message)s")
    if not sys.platform.startswith("win") and sys.stderr.isatty():
        def add_color_emit_ansi(fn):
            """Add methods we need to the class."""
            def new(*args):
                """Method overload."""
                if len(args) == 2:
                    new_args = (args[0], copy(args[1]))
                else:
                    new_args = (args[0], copy(args[1]), args[2:])
                if hasattr(args[0], 'baseFilename'):
                    return fn(*args)
                levelno = new_args[1].levelno
                if levelno >= 50:
                    color = '\x1b[31;5;7m\n '  # blinking red with black
                elif levelno >= 40:
                    color = '\x1b[31m'  # red
                elif levelno >= 30:
                    color = '\x1b[33m'  # yellow
                elif levelno >= 20:
                    color = '\x1b[32m'  # green
                elif levelno >= 10:
                    color = '\x1b[35m'  # pink
                else:
                    color = '\x1b[0m'  # normal
                try:
                    new_args[1].msg = color + str(new_args[1].msg) + ' \x1b[0m'
                except Exception as reason:
                    print(reason)  # Do not use log here.
                return fn(*new_args)
            return new
        # all non-Windows platforms support ANSI Colors so we use them
        log.StreamHandler.emit = add_color_emit_ansi(log.StreamHandler.emit)
    else:
        log.debug("Colored Logs not supported on {0}.".format(sys.platform))
    return log


def main():
    """Main Loop."""
    make_logger("unicodemoticon")
    make_root_check_and_encoding_debug()
    set_process_name_and_cpu_priority("unicodemoticon")
    set_single_instance("unicodemoticon")
    signal.signal(signal.SIGINT, signal.SIG_DFL)  # CTRL+C work to quit app
    app = QApplication(sys.argv)
    app.setApplicationName("unicodemoticon")
    app.setOrganizationName("unicodemoticon")
    app.setOrganizationDomain("unicodemoticon")
    app.instance().setQuitOnLastWindowClosed(False)  # no quit on dialog close
    icon = QIcon(app.style().standardPixmap(QStyle.SP_FileIcon))
    app.setWindowIcon(icon)
    win = MainWindow(icon)
    win.show()
    make_post_execution_message()
    sys.exit(app.exec())


if __name__ in '__main__':
    main()


# kate: space-indent on; indent-width 4;
