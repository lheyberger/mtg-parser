#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from mtg_parser.card import Card


__all__ = []


def can_handle(src):
    return (
        isinstance(src, str)
        and
        re.match(r'(?:https?://)?(?:www\.)?aetherhub\.com', src)
    )


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
            if last_category:
                tags = [last_category]
            card = Card(name, quantity, extension, number, tags)
            yield card
