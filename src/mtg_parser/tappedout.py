#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from mtg_parser.decklist import parse_deck as decklist_parse_deck


__all__ = []


def can_handle(src):
    return (
        isinstance(src, str)
        and
        src.strip().startswith('https://tappedout.net/mtg-decks/')
    )


def parse_deck(src):
    return _parse_deck(_download_deck(src))


def _download_deck(src):
    result = requests.get(src)
    pattern = r'.*<textarea.*?id="mtga-textarea".*?>(.*?)\s*</textarea>'
    match = re.match(pattern, result.text, re.M | re.S)
    return match.group(1)


def _parse_deck(deck):
    return decklist_parse_deck(deck)
