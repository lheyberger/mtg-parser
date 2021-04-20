#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from mtg_parser.card import Card


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
            yield Card(
                row.a.string.strip(),
                row.td.string.strip(),
                re.search(
                    r'\[(.*?)\]',
                    row.a.attrs.get('data-card-id')
                ).group(1).lower(),
                tags=[last_category],
            )
