#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from mtg_parser.card import Card


__all__ = []


def can_handle(src):
    return (
        isinstance(src, str)
        and
        re.match(r'(?:https?://)?(?:www\.)?mtggoldfish\.com/deck/', src)
    )


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
