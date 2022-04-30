#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from mtg_parser.card import Card


__all__ = []


def can_handle(src):
    return (
        isinstance(src, str)
        and
        re.match(r'https?://.*?moxfield\.com', src)
    )


def parse_deck(src):
    deck = None
    if can_handle(src):
        deck = _parse_deck(_download_deck(src))
    return deck


def _download_deck(src):
    url = 'https://api.moxfield.com/v2/decks/all/{}'.format(
        re.search(r'https://.*?moxfield.com/.*/([a-zA-Z0-9-_]+)', src).group(1)
    )
    return requests.get(url).json()


def _parse_deck(deck):
    for key, value in deck['commanders'].items():
        yield Card(key, value['quantity'], tags=['commander'])

    for key, value in deck['companions'].items():
        yield Card(key, value['quantity'], tags=['companion'])

    for key, value in deck['mainboard'].items():
        yield Card(key, value['quantity'])
