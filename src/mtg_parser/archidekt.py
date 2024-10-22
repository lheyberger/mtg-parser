#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from mtg_parser.card import Card
from mtg_parser.utils import build_pattern, match_pattern


__all__ = []


_PATTERN = build_pattern('archidekt.com', r'/decks/(?P<deck_id>\d+)/?')


def can_handle(src):
    return match_pattern(src, _PATTERN)


def parse_deck(src, session=requests):
    deck = None
    if can_handle(src):
        deck = _parse_deck(_download_deck(src, session))
    return deck


def _download_deck(src, session):
    deck_id = re.search(_PATTERN, src).group('deck_id')
    url = f"https://www.archidekt.com/api/decks/{deck_id}/"
    return session.get(url).json()


def _parse_deck(deck):
    categories = deck['categories']
    categories = filter(lambda c: c.get('includedInDeck', False), categories)
    categories = map(lambda c: c['name'], categories)
    categories = set(categories)
    for card in deck['cards']:
        if not card['categories'] or categories & set(card['categories']):
            yield Card(
                card['card']['oracleCard']['name'],
                card['quantity'],
                card['card']['edition']['editioncode'],
                card['card'].get('collectorNumber'),
                card['categories']
            )
