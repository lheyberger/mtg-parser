#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


__all__ = [
    'get_moxfield_deck',
    'parse_moxfield_deck',
]


def _get_card_data(key, value):
    return {
        'quantity': value['quantity'],
        'card_name': key,
        'scryfall_url': 'https://api.scryfall.com/cards/{}'.format(
            value['card']['scryfall_id']
        )
    }


def parse_moxfield_deck(deck):
    for key, value in deck['commanders'].items():
        card = _get_card_data(key, value)
        card.setdefault('tags', []).append('commander')
        yield card

    for key, value in deck['companions'].items():
        card = _get_card_data(key, value)
        card.setdefault('tags', []).append('companion')
        yield card

    for key, value in deck['mainboard'].items():
        card = _get_card_data(key, value)
        yield card


def get_moxfield_deck(moxfield_id):
    url = 'https://api.moxfield.com/v2/decks/all/{}'.format(moxfield_id)
    result = requests.get(url)
    return result.json()
