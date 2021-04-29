#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import requests
from mtg_parser.card import Card


__all__ = []


def can_handle(src):
    return (
        isinstance(src, str)
        and
        bool(re.match(r'https://deckstats.net/decks/\d+/\d+-.*', src))
    )


def parse_deck(src):
    deck = None
    if can_handle(src):
        deck = _parse_deck(_download_deck(src))
    return deck


def _download_deck(src):
    result = requests.get(src).text.splitlines()
    result = next(line for line in result if 'init_deck_data' in line)
    result = re.match(r'.*init_deck_data\((.*?)\);', result)
    return json.loads(result.group(1))


def _parse_deck(deck):
    for section in deck.get('sections', []):
        for card in section.get('cards', {}):
            yield Card(
                card['name'],
                card['amount'],
                tags=_get_tags(card),
            )


def _get_tags(card):
    if card.get('isCommander', False):
        yield 'commander'
    if card.get('isCompanion', False):
        yield 'companion'
