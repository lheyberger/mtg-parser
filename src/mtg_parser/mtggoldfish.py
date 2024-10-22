#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from mtg_parser.card import Card
from mtg_parser.utils import build_pattern, match_pattern


__all__ = []


_PATTERN = build_pattern('mtggoldfish.com', r'/deck/(?P<deck_id>\d+)/?')


def can_handle(src):
    return match_pattern(src, _PATTERN)


def parse_deck(src, session=requests):
    deck = None
    if can_handle(src):
        deck = _parse_deck(_download_deck(src, session))
    return deck


def _download_deck(src, session):
    return session.get(src, headers={'Accept': 'text/html'}).text


def _parse_deck(deck):
    soup = BeautifulSoup(deck, features='html.parser')
    soup = soup.find('table', class_='deck-view-deck-table')
    soup = soup.find_all('tr', recursive=False)

    last_category = None
    for row in soup:
        if 'deck-category-header' in row.attrs.get('class', []):
            last_category = row.th.get_text(strip=True).strip().splitlines()[0].lower()
        else:
            yield Card(
                row.a.string.strip(),
                row.td.string.strip(),
                re.search(
                    r'\[(.*?)\]',
                    row.a.attrs.get('data-card-id')
                ).group(1).lower(),
                tags=[last_category],
            )
