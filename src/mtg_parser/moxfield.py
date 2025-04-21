#!/usr/bin/env python

import re

import httpx

from mtg_parser.card import Card
from mtg_parser.utils import build_pattern, match_pattern


__all__ = []


_PATTERN = build_pattern('moxfield.com', r'/decks/(?P<deck_id>[a-zA-Z0-9-_]+)/?')


def can_handle(src):
    return match_pattern(src, _PATTERN)


def parse_deck(src, http_client=None):
    deck = None
    if can_handle(src):
        http_client = http_client or httpx.Client()
        with http_client:
            deck = _parse_deck(_download_deck(src, http_client))
    return deck


def _download_deck(src, http_client):
    deck_id = re.search(_PATTERN, src).group('deck_id')
    url = f"https://api.moxfield.com/v2/decks/all/{deck_id}"
    response = http_client.head(src)
    response = http_client.get(url)
    return response.json()


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
