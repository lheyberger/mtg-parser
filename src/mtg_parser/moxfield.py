#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests


__all__ = []


def can_handle(src):
    return (
        isinstance(src, str)
        and
        src.strip().startswith('https://api.moxfield.com/v2/decks/all/')
    )


def parse_deck(src):
    return _parse_deck(_download_deck(src))


def _download_deck(src):
    return requests.get(src).json()


def _parse_deck(deck):
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


def _get_card_data(key, value):
    return {
        'quantity': value['quantity'],
        'card_name': key,
        'scryfall_url': 'https://api.scryfall.com/cards/{}'.format(
            value['card']['scryfall_id']
        )
    }
