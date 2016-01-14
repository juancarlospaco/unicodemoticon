#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# metadata
"""UnicodEmoticons."""
__version__ = '1.4.0'
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
import socket
import sys
import time
import unicodedata
from copy import copy
from ctypes import byref, cdll, create_string_buffer
from datetime import datetime
from getopt import getopt
from html import entities
from os import path
from platform import platform, python_version
from random import randint
from subprocess import call
from tempfile import gettempdir
from urllib import request
from webbrowser import open_new_tab

from PyQt5.QtCore import Qt, QTimer, QUrl

from PyQt5.QtGui import QColor, QCursor, QFont, QIcon, QPainter, QPalette, QPen

from PyQt5.QtNetwork import (QNetworkAccessManager, QNetworkProxyFactory,
                             QNetworkRequest)

from PyQt5.QtWidgets import (QAction, QApplication, QInputDialog, QLabel,
                             QMenu, QMessageBox, QProgressDialog, QStyle,
                             QSystemTrayIcon)

try:
    import resource  # windows dont have resource
except ImportError:
    resource = None

try:
    import qdarkstyle  # https://github.com/ColinDuquesnoy/QDarkStyleSheet
except ImportError:    # sudo pip3 install qdarkstyle
    qdarkstyle = None  # 100% optional


QSS_STYLE = "/* Write your Custom Styles here */"

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
X-KDE-StartupNotify=false"""

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
         "(づ ￣ ³￣)づ ⓈⓂⓄⓄⓉⒽ", "❚█══█❚ ▐━━━━━▌"),

    "multi-character 3":
        ("/( ͡° ͜ʖ ͡° )つ──☆*:・ﾟ", "(ง⌐□ل͜□)ง", " ─=≡Σ((( つ◕ل͜◕)つ",
         " ┬──┬◡ﾉ(° -°ﾉ)", "(•̀ᴗ•́)و ̑̑", "（。Y。）ԅ(≖‿≖ԅ)", "(っ˘з(˘⌣˘ )",
         "(ᗒᗣᗕ)՞", "¯\_( ʘ‿ʘ)人(ʘ‿ʘ )_/¯", "ฅ(⌯͒• ɪ •⌯͒)ฅ❣","ฅ(≚ᄌ≚) ",
         "o(≧∇≦o)", "ฅ ̳͒•ˑ̫• ̳͒ฅ", "(=｀ェ´=)", "₍˄ุ.͡˳̫.˄ุ₎ฅ˒˒", "༼༭ຶཬ༤ຶ༽", "૮(ㅍ◞◟ㅍ)ა",
         "(〓￣(∵エ∵)￣〓)", "૮(꒦ິཅ꒦ິ)ა", "✲ﾟ｡✧٩(･ิᴗ･ิ๑)۶✲ﾟ｡✧", "٩(๑ơలơ)۶♡",
         "- =͟͟͞͞ ( ꒪౪꒪)ฅ✧", "୧( ॑ധ ॑)୨", "(Ɔ ˘⌣˘)♥(˘⌣˘ C)", "(ʃƪ ˘ ³˘)",
         "♡ლ(-༗‿༗-)ლ♡", "\(≚ᄌ≚)/", "＼⍩⃝／", "(ಠ .̫.̫ ಠ)",
         "( • Y • )ԅ(‾⌣‾ԅ)", "૮(⋆❛ہ❛⋆)ა", "/(　-̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥᷄◞ω◟-̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥̥᷅ )", "૮(꒦ິཅ꒦ິ)ა",
         "\(¬ω¬)/", "¯\_(҂⌣̀_⌣́)_/¯", "ლ(´﹏`ლ)", "\( ༎ຶŎ༎ຶ )/",
         "ღ╰⋃╯ღ•̥̑ .̮ •̥̑)", "⊂(^(工)^)⊃", "|'''\ (Ⓘ.Ⓘ) /'''|",
         "ヽ(´ー`)人(´∇｀)人(`Д´)ノ", "ʕʘ̅͜ʘ̅ʔ", "¯\_(❤‿❤)_/¯")
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


###############################################################################


class MainWindow(QSystemTrayIcon):

    """Main widget for UnicodEmoticons,not really a window since not needed."""

    def __init__(self, icon, parent=None):
        """Tray icon main widget."""
        super(MainWindow, self).__init__(icon, parent)
        log.debug("Starting {}.".format(__doc__))
        self.setIcon(icon)
        self.setToolTip(__doc__ + "\nPick 1 Emoticon, use CTRL+V to Paste it!")
        self.traymenu = QMenu("Emoticons")
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
        menu_html.setToolTipsVisible(True)
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
                    try:
                        action.setToolTip(
                            unicodedata.name(html_char[1]).title())
                    except ValueError:
                        pass
        self.traymenu.addAction("AlTeRnAtE-CaSe", self.make_alternate_case)
        self.traymenu.addAction("Explain Unicode", self.make_explain_unicode)
        self.traymenu.addAction("Search Unicode", self.make_search_unicode)
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
    def make_explain_unicode(self) -> tuple:
        """Make an explanation from unicode entered,if at least 1 chars."""
        explanation, uni = "", None
        uni = str(QInputDialog.getText(
            None, __doc__, "<b>Type Unicode character to explain?")[0]).strip()
        if uni and len(uni):
            explanation = ", ".join([unicodedata.name(_).title() for _ in uni])
            QMessageBox.information(None, __doc__, str((uni, explanation)))
        log.debug((uni, explanation))
        return (uni, explanation)

    def make_search_unicode(self):
        """Make a Pop-Up Dialog to search Unicode Emoticons."""
        sorry = "<i>Nothing found! Search can not find similar Unicode, sorry."
        search = str(QInputDialog.getText(
            None, __doc__, "<b>Type to search Unicode ?:")[0]).lower()
        if search and len(search.strip()):
            log.debug("Searching all Unicode for: '{0}'.".format(search))
            found_exact = [_ for _ in UNICODEMOTICONS.values() if search in _]
            found_by_name = []
            for emoticons_list in UNICODEMOTICONS.values():
                for emote in emoticons_list:
                    try:
                        emoticon_name = unicodedata.name(emote).lower().strip()
                    except Exception:
                        emoticon_name = ""
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
    ram_use, ram_all = 0, 0
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
    G+: https://plus.google.com/share?url={u}\nSend BitCoins !: 
    https://www.coinbase.com/checkouts/c3538d335faee0c30c81672ea0223877
    """.format(u=__url__, n=app)))
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
    sys.dont_write_bytecode = True
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
    if qdarkstyle:
            app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    icon = QIcon(app.style().standardPixmap(QStyle.SP_FileIcon))
    app.setWindowIcon(icon)
    win = MainWindow(icon)
    win.show()
    make_post_execution_message()
    sys.exit(app.exec())


if __name__ in '__main__':
    main()


# kate: space-indent on; indent-width 4;
