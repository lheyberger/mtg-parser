#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from mtg_parser.card import Card


__all__ = []


def can_handle(src):
    return (
        isinstance(src, str)
        and
        re.match(r'(https?://)?(www\.)?archidekt\.com', src)
    )


def parse_deck(src):
    deck = None
    if can_handle(src):
        deck = _parse_deck(_download_deck(src))
    return deck


def _download_deck(src):
    url = 'https://www.archidekt.com/api/decks/{}/small/'.format(
        re.search(r'decks/(\d+)', src).group(1)
    )
    return requests.get(url).json()


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
