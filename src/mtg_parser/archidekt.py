#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from mtg_parser.utils import get_scryfall_url


__all__ = []


def parse_deck(src):
    deck = None
    if _can_handle(src):
        deck = _parse_deck(_download_deck(src))
    return deck


def _can_handle(src):
    return (
        isinstance(src, str)
        and
        src.startswith('https://www.archidekt.com')
    )


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
        if categories.intersection(card['categories']):
            yield _get_card_data(card)


def _get_card_data(card):
    quantity = card['quantity']
    card_name = card['card']['oracleCard']['name']
    extension = card['card']['edition']['editioncode']
    collector_number = card['card'].get('collectorNumber')
    scryfall_url = get_scryfall_url(card_name, extension, collector_number)
    tags = list(map(str.lower, card['categories']))
    return {
        'quantity': quantity,
        'card_name': card_name,
        'extension': extension,
        'collector_number': collector_number,
        'scryfall_url': scryfall_url,
        'tags': tags,
    }
