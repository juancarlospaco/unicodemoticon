#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Custom tab widget."""


import codecs
import re

from base64 import b64encode, urlsafe_b64encode
from locale import getdefaultlocale
from urllib import parse

from PyQt5.QtWidgets import (QComboBox, QHBoxLayout, QLabel, QLineEdit,
                             QPushButton, QWidget)

from .scrollgroup import ScrollGroup
from .tinyslation import tinyslation


_CODES = tuple("""aa ab ae af ak am an ar as av ay az ba be bg bh bi bm bn bo
bo br bs ca ce ch co cr cs cs cu cv cy cy da de de dv dz ee el el en eo es et
eu eu fa fa ff fi fj fo fr fr fy ga gd gl gn gu gv ha he hi ho hr ht hu hy hy
hz ia id ie ig ii ik io is is it iu ja jv ka kg ki kj kk kl km kn ko kr ks ku
kv kw ky la lb lg li ln lo lt lu lv mg mh mi mi mk mk ml mn mr ms ms mt my my
na nb nd ne ng nl nl nn no nr nv oc oj om or os pa pi pl ps pt qu rm rn ro ro
ru rw sa sc sd se sg si sk sk sl sm sn so sq sq sr ss st su sv sw ta te tg th
ti tk tl tn to tr ts tt tw ty ug uk ur uz ve vi vo wa wo xh yi yo za zh zh zu
""".split())


class TabTool(ScrollGroup):

    """Custom tab widget."""

    def __init__(self, parent=None, *args, **kwargs):
        """Init class custom tab widget."""
        super(TabTool, self).__init__(self, *args, **kwargs)
        self.parent = parent
        self.setParent(parent)

        self.inputx, self.alt, self.b64 = QLineEdit(), QLineEdit(), QLineEdit()
        self.b64unsafe, self.rot13 = QLineEdit(), QLineEdit()
        self.urlenc, self.urlencp = QLineEdit(), QLineEdit()
        self.snake, self.spine = QLineEdit(), QLineEdit()
        self.asci, self.camel, self.swp = QLineEdit(), QLineEdit(), QLineEdit()
        self.tran, self.fr, self.to = QLineEdit(), QComboBox(), QComboBox()
        self.container, loca = QWidget(), str(getdefaultlocale()[0][:2])
        self.fr.addItems(_CODES)
        self.to.addItems(_CODES)
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

        layout = self.layout()
        layout.addWidget(QLabel("<h1>Type or Paste text"), 0, 0)
        layout.addWidget(self.inputx, 1, 0)
        layout.addWidget(self.runtools, 2, 0)
        layout.addWidget(QLabel("Translated Text"), 3, 0)
        layout.addWidget(self.container, 4, 0)
        layout.addWidget(QLabel("Alternate case"), 5, 0)
        layout.addWidget(self.alt, 6, 0)
        layout.addWidget(QLabel("Swap case"), 7, 0)
        layout.addWidget(self.swp, 8, 0)
        layout.addWidget(QLabel("Base 64 URL Safe, for the Web"), 9, 0)
        layout.addWidget(self.b64, 10, 0)
        layout.addWidget(QLabel("Base 64"), 11, 0)
        layout.addWidget(self.b64unsafe, 12, 0)
        layout.addWidget(QLabel("ROT-13"), 13, 0)
        layout.addWidget(self.rot13, 14, 0)
        layout.addWidget(QLabel("URL Encode Plus+"), 15, 0)
        layout.addWidget(self.urlencp, 16, 0)
        layout.addWidget(QLabel("URL Encode"), 17, 0)
        layout.addWidget(self.urlenc, 18, 0)
        layout.addWidget(QLabel("Camel Case"), 19, 0)
        layout.addWidget(self.camel, 20, 0)
        layout.addWidget(QLabel("Snake Case"), 21, 0)
        layout.addWidget(self.snake, 22, 0)
        layout.addWidget(QLabel("Spine Case"), 23, 0)
        layout.addWidget(self.spine, 24, 0)
        layout.addWidget(QLabel("Sanitized, Pure ASCII"), 25, 0)
        layout.addWidget(self.asci, 26, 0)

    def runtool(self, *args):
        """Run all text transformation tools."""
        txt = str(self.inputx.text()).strip()
        if not len(txt):
            return
        for field in (
            self.alt, self.b64, self.b64unsafe, self.rot13, self.urlenc,
            self.urlencp, self.snake, self.spine, self.asci, self.camel,
                self.swp, self.tran):
            field.clear()
            field.setReadOnly(True)
        self.alt.setText(self.parent.make_alternate_case(txt))
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
        if self.fr.currentText() != self.to.currentText() and len(txt) < 999:
            self.tran.setText(tinyslation(txt.strip().replace("\n", " "),
                              str(self.to.currentText()),
                              str(self.fr.currentText())))
