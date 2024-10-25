#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from mtg_parser.card import Card
from mtg_parser.utils import build_pattern, match_pattern


__all__ = []


_PATTERN = build_pattern('aetherhub.com', r'/Deck/(?P<deck_id>.+)/?')


def can_handle(src):
    return match_pattern(src, _PATTERN)


def parse_deck(src, session=requests):
    deck = None
    if can_handle(src):
        deck = _parse_deck(_download_deck(src, session))
    return deck


def _download_deck(src, session):
    result = session.get(src).text
    soup = BeautifulSoup(result, features='html.parser')
    element = soup.find(attrs={'data-deckid': True})
    deck_id = element['data-deckid']

    return session.get(
        'https://aetherhub.com/Deck/FetchMtgaDeckJson',
        params={
            'deckId': deck_id,
            'langId': 0,
            'simple': False,
        }
    ).json()


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
