#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


__all__ = [
    'get_archidekt_deck',
    'parse_archidekt_deck',
]


def _get_card_data(card):
    extension = card['card']['edition']['editioncode']
    collector_number = card['card']['collectorNumber']
    scryfall_url = 'https://api.scryfall.com/cards/{}/{}'.format(
        extension,
        collector_number
    )
    return {
        'quantity': card['quantity'],
        'card_name': card['card']['oracleCard']['name'],
        'extension': extension,
        'collector_number': collector_number,
        'scryfall_url': scryfall_url,
        'tags': list(map(str.lower, card['categories'])),
    }


def parse_archidekt_deck(deck):
    categories = deck['categories']
    categories = filter(lambda c: c['includedInDeck'], categories)
    categories = map(lambda c: c['name'], categories)
    categories = set(categories)

    for card in deck['cards']:
        if categories.intersection(card['categories']):
            yield _get_card_data(card)


def get_archidekt_deck(archidekt_id):
    url = 'https://www.archidekt.com/api/decks/{}/'.format(archidekt_id)
    result = requests.get(url)
    return result.json()
