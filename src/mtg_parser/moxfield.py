#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from mtg_parser.card import Card


__all__ = []


_DOMAIN_PATTERN = r'(?:https?://)?.*?moxfield\.com'
_PATH_PATTERN = r'/.*/'
_ID_PATTERN = r'([a-zA-Z0-9-_]+)'


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
    pattern = _DOMAIN_PATTERN + _PATH_PATTERN + _ID_PATTERN
    deck_id = re.search(pattern, src).group(1)
    url = f"https://api.moxfield.com/v2/decks/all/{deck_id}"
    return session.get(url).json()


def _parse_deck(deck):
    for key, value in deck['commanders'].items():
        yield Card(key, **_extract_information(value), tags=['commander'])

    for key, value in deck['companions'].items():
        yield Card(key, **_extract_information(value), tags=['companion'])

    for key, value in deck['mainboard'].items():
        yield Card(key, **_extract_information(value))


def _extract_information(card):
    return {
        'quantity': card.get('quantity', 1),
        'extension': card.get('card', {}).get('set'),
        'number': card.get('card', {}).get('cn'),
    }
