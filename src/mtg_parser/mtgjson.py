#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from mtg_parser.card import Card
from mtg_parser.utils import build_pattern, match_pattern


__all__ = []


_PATTERN = build_pattern('mtgjson.com', r'/api/v5/decks/(?P<deck_id>.+\.json)')


def can_handle(src):
    return match_pattern(src, _PATTERN)


def parse_deck(src, session=requests):
    deck = None
    if can_handle(src):
        deck = _parse_deck(_download_deck(src, session))
    return deck


def _download_deck(src, session):
    return session.get(src).json()


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
