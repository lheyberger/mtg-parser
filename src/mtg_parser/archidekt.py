#!/usr/bin/env python

import re

import httpx

from mtg_parser.card import Card
from mtg_parser.utils import build_pattern, match_pattern


__all__ = []


_PATTERN = build_pattern('archidekt.com', r'/decks/(?P<deck_id>\d+)/?')


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
    url = f"https://archidekt.com/api/decks/{deck_id}/"
    response = http_client.get(url)
    return response.json()


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
                card['categories'],
            )
