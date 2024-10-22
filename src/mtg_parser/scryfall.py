#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import re
import csv
import requests
from mtg_parser.card import Card
from mtg_parser.utils import build_pattern, match_pattern


__all__ = []


_PATTERN = build_pattern(
    'scryfall.com',
    r'/(?P<user_id>@.+)/decks/(?P<deck_id>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/?',
)


def can_handle(src):
    return match_pattern(src, _PATTERN)


def parse_deck(src, session=requests):
    deck = None
    if can_handle(src):
        deck = _parse_deck(_download_deck(src, session))
    return deck


def _download_deck(src, session):
    deck_id = re.search(_PATTERN, src).group('deck_id')
    url = f"https://api.scryfall.com/decks/{deck_id}/export/csv"
    return session.get(url).text


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
