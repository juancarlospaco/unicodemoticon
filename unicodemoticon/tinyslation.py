#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""Translate from internet via API from mymemory.translated.net,legally."""


from locale import getdefaultlocale
from urllib import parse, request
from json import loads


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
