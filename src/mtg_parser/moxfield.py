#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests


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
        re.match(r'https://.*?moxfield.com', src)
    )


def _download_deck(src):
    url = 'https://api.moxfield.com/v2/decks/all/{}'.format(
        re.search(r'https://.*?moxfield.com/.*/([a-zA-Z0-9]+)', src).group(1)
    )
    return requests.get(url).json()


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
