#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
from mtg_parser.card import Card
from mtg_parser.utils import build_pattern, match_pattern


__all__ = []


_PATTERN = build_pattern('deckstats.net', r'/decks/(?P<user_id>\d+)/(?P<deck_id>\d+-.*)/?')


def can_handle(src):
    return match_pattern(src, _PATTERN)


def parse_deck(src, session=requests):
    deck = None
    if can_handle(src):
        deck = _parse_deck(_download_deck(src, session))
    return deck


def _download_deck(src, session):
    start_token = 'init_deck_data('
    end_token = ');'

    result = session.get(src).text.splitlines()
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
