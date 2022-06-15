#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from mtg_parser.decklist import parse_deck as decklist_parse_deck


__all__ = []


_DOMAIN_PATTERN = r'(?:https?://)?(?:www\.)?scryfall\.com'
_PATH_PATTERN = r'/.*decks/'
_GUID_PATTERN = r'(\w{8}-\w{4}-\w{4}-\w{4}-\w{12})'


def can_handle(src):
    return (
        isinstance(src, str)
        and
        re.match(_DOMAIN_PATTERN, src)
    )


def parse_deck(src, session=requests):
    deck = None
    if can_handle(src):
        deck = _parse_deck(_download_deck(src, session))
    return deck


def _download_deck(src, session):
    pattern = _DOMAIN_PATTERN + _PATH_PATTERN + _GUID_PATTERN
    url = 'https://api.scryfall.com/decks/{}/export/text'.format(
        re.search(pattern, src).group(1)
    )
    return session.get(url).text


def _parse_deck(deck):
    return decklist_parse_deck(deck)
