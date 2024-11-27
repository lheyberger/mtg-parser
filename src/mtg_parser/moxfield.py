#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import requests
from mtg_parser.card import Card
from mtg_parser.utils import build_pattern, match_pattern


__all__ = []


_PATTERN = build_pattern('moxfield.com', r'/decks/(?P<deck_id>[a-zA-Z0-9-_]+)/?')


def can_handle(src):
    return match_pattern(src, _PATTERN)


def parse_deck(src, session=requests):
    deck = None
    if can_handle(src):
        deck = _parse_deck(_download_deck(src, session))
    return deck


def _download_deck(src, session):
    moxfield_user_agent = os.getenv('MOXFIELD_USER_AGENT')
    headers = {
        'User-Agent': moxfield_user_agent
    } if moxfield_user_agent else {}

    deck_id = re.search(_PATTERN, src).group('deck_id')
    url = f"https://api.moxfield.com/v2/decks/all/{deck_id}"
    return session.get(url, headers=headers).json()


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
