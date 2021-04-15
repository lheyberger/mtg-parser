#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
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
        bool(re.match(r'https://deckstats.net/decks/\d+/\d+-.*', src))
    )


def _download_deck(src):
    result = requests.get(src).text.splitlines()
    result = next(line for line in result if 'init_deck_data' in line)
    result = re.match(r'.*init_deck_data\((.*?)\);', result)
    return json.loads(result.group(1))


def _parse_deck(deck):
    for section in deck.get('sections', []):
        for card in section.get('cards', {}):
            yield _get_card_data(card)


def _get_card_data(card):
    tags = []
    if card.get('isCommander', False):
        tags.append('commander')
    tags.append(card['data']['supertype_group_extended'].lower())
    return {
        'quantity': card['amount'],
        'card_name': card['name'],
        'scryfall_url': get_scryfall_url(card.get('name')),
        'tags': tags,
    }
