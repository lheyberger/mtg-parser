#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import requests
from .utils import scryfal_url_from_name


__all__ = [
    'get_deckstats_deck',
    'parse_deckstats_deck',
]


def _get_card_data(card):
    tags = []
    if card.get('isCommander', False):
        tags.append('commander')
    tags.append(card['data']['supertype_group_extended'].lower())
    return {
        'quantity': card['amount'],
        'card_name': card['name'],
        'scryfall_url': scryfal_url_from_name(card['name']),
        'tags': tags,
    }


def parse_deckstats_deck(deck):
    for section in deck.get('sections', []):
        for card in section.get('cards', {}):
            yield _get_card_data(card)


def get_deckstats_deck(deckstats_id):
    url = 'https://deckstats.net/decks/{}'.format(deckstats_id)
    result = requests.get(url).text.splitlines()
    result = next(line for line in result if 'init_deck_data' in line)
    result = re.match(r'.*init_deck_data\((.*?)\);', result)
    return json.loads(result.group(1))
