#!/usr/bin/env python

import csv
import io
import re

import httpx

from mtg_parser.card import Card
from mtg_parser.utils import build_pattern, match_pattern


__all__ = []


_PATTERN = build_pattern(
    'scryfall.com',
    r'/(?P<user_id>@.+)/decks/(?P<deck_id>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/?',
)


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
    deck_id = re.search(_PATTERN, src).group('deck_id')
    url = f"https://api.scryfall.com/decks/{deck_id}/export/csv"
    response = http_client.get(url)
    return response.text


def _parse_deck(deck):
    deck_csv = io.StringIO(deck)
    reader = csv.DictReader(deck_csv)
    for card in reader:
        yield Card(
            card['name'],
            int(card['count']),
            card['set_code'],
            card['collector_number'],
            tags=_get_tags(card['section']),
        )


def _get_tags(section_name: str):
    if section_name and section_name.lower() == 'commanders':
        yield 'commander'
    if section_name and section_name.lower() == 'outside':
        yield 'companion'
