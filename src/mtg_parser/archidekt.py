#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


__all__ = []


def can_handle(src):
    return (
        isinstance(src, str)
        and
        src.strip().startswith('https://www.archidekt.com/api/decks/')
    )


def parse_deck(src):
    return _parse_deck(_download_deck(src))


def _download_deck(src):
    return requests.get(src).json()


def _parse_deck(deck):
    categories = deck['categories']
    categories = filter(lambda c: c['includedInDeck'], categories)
    categories = map(lambda c: c['name'], categories)
    categories = set(categories)

    for card in deck['cards']:
        if categories.intersection(card['categories']):
            yield _get_card_data(card)


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
