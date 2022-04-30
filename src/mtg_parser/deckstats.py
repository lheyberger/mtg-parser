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
        re.match(r'https?://deckstats\.net/decks/\d+/\d+-.*', src)
    )


def parse_deck(src):
    deck = None
    if can_handle(src):
        deck = _parse_deck(_download_deck(src))
    return deck


def _download_deck(src):
    start_token = 'init_deck_data('
    end_token = ');'

    result = requests.get(src).text.splitlines()
    result = next(line for line in result if start_token in line)

    result = result[result.find(start_token) + len(start_token):]
    result = result[:result.find(end_token)]

    i = 0
    opened = 0
    for i, char in enumerate(result):
        if char == '{':
            opened = opened + 1
        if char == '}':
            opened = opened - 1
        if opened <= 0:
            break
    result = result[:i+1]
    return json.loads(result)


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
