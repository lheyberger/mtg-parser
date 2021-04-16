#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
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
        src.strip().startswith('https://www.mtggoldfish.com/deck/')
    )


def _download_deck(src):
    return requests.get(src).text


def _parse_deck(deck):
    soup = BeautifulSoup(deck, features='html.parser')
    soup = soup.find('table', class_='deck-view-deck-table')
    soup = soup.find_all('tr', recursive=False)

    last_category = None
    for row in soup:
        if 'deck-category-header' in row.attrs.get('class', []):
            last_category = row.th.string.strip().splitlines()[0].lower()
        else:
            extension = re.search(
                r'\[(.*?)\]',
                row.a.attrs.get('data-card-id')
            ).group(1).lower()
            card_name = row.a.string.strip()
            card = {
                'quantity': row.td.string.strip(),
                'card_name': card_name,
                'extension': extension,
                'scryfall_url': get_scryfall_url(card_name, extension),
            }
            if last_category:
                card.setdefault('tags', []).append(last_category)
            yield card
