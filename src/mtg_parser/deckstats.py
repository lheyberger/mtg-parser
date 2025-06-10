#!/usr/bin/env python

import json

import httpx

from mtg_parser.card import Card
from mtg_parser.utils import build_pattern, match_pattern


__all__ = []


_PATTERN = build_pattern('deckstats.net', r'/decks/(?P<user_id>\d+)/(?P<deck_id>\d+-.*)/?')


def can_handle(src):
    return match_pattern(src, _PATTERN)


def parse_deck(src, http_client=None):
    deck = None
    if can_handle(src):
        http_client = http_client or httpx.Client()
        with http_client:
            deck = _parse_deck(_download_deck(src, http_client))
    return deck


def _download_deck(src, http_client):
    start_token = 'init_deck_data(' # noqa: S105
    end_token = ');' # noqa: S105

    result = http_client.get(src).text.splitlines()
    result = next(line for line in result if start_token in line)

    result = result[result.find(start_token) + len(start_token):]
    result = result[:result.find(end_token)]

    _i = 0
    opened = 0
    for _i, char in enumerate(result):
        if char == '{':
            opened = opened + 1
        if char == '}':
            opened = opened - 1
        if opened <= 0:
            break
    result = result[:_i+1]
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
