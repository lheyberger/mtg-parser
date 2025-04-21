#!/usr/bin/env python

import httpx

from mtg_parser.card import Card
from mtg_parser.utils import build_pattern, match_pattern


__all__ = []


_PATTERN = build_pattern('mtgjson.com', r'/api/v5/decks/(?P<deck_id>.+\.json)')


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
    response = http_client.get(src)
    return response.json()


def _parse_deck(deck):
    for card in deck.get('data', {}).get('commander', []):
        yield Card(
            card['name'],
            quantity=card['count'],
            extension=card['setCode'],
            tags=['commander'],
        )

    for card in deck.get('data', {}).get('mainBoard', []):
        yield Card(
            card['name'],
            quantity=card['count'],
            extension=card['setCode'],
        )
