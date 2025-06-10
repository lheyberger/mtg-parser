#!/usr/bin/env python

import httpx
from bs4 import BeautifulSoup

from mtg_parser.card import Card
from mtg_parser.utils import build_pattern, match_pattern


__all__ = []


_PATTERN = build_pattern('aetherhub.com', r'/Deck/(?P<deck_id>.+)/?')


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
    result = http_client.get(src).text
    soup = BeautifulSoup(result, features='html.parser')
    element = soup.find(attrs={'data-deckid': True})
    deck_id = element['data-deckid']

    response = http_client.get(
        'https://aetherhub.com/Deck/FetchMtgaDeckJson',
        params={
            'deckId': deck_id,
            'langId': 0,
            'simple': False,
        },
    )
    return response.json()


def _parse_deck(deck):
    last_category = None
    for entry in deck.get('convertedDeck', []):
        quantity = entry.get('quantity')
        name = entry.get('name')
        extension = entry.get('set')
        number = entry.get('number')
        if not quantity:
            last_category = name
        elif name and quantity:
            tags = [last_category] if last_category else None
            card = Card(name, quantity, extension, number, tags)
            yield card
