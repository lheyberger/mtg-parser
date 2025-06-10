#!/usr/bin/env python

import html
import re

import httpx
from bs4 import BeautifulSoup

from mtg_parser.card import Card
from mtg_parser.utils import build_pattern, match_pattern


__all__ = []


_PATTERN = build_pattern('mtggoldfish.com', r'/deck/(?P<deck_id>\d+)/?')


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
    response = http_client.get(src, headers={'Accept': 'text/html'})
    soup = BeautifulSoup(response.text, features='html.parser')
    csrf_token = (soup.find('meta', attrs={'name': 'csrf-token'}) or {}).get('content')

    deck_id = re.search(_PATTERN, src).group('deck_id')
    url = f"https://www.mtggoldfish.com/deck/component?id={deck_id}"
    headers = {
        'X-CSRF-Token': csrf_token,
        'X-Requested-With': 'XMLHttpRequest',
    }
    response = http_client.get(url, headers=headers)
    return response.text


def _parse_deck(deck):
    deck = deck.splitlines()[0]
    deck = deck.replace("\\'", "'").replace('\\"', '"').replace("\\/", "/").replace(r"\n", "")
    deck = html.unescape(deck)

    soup = BeautifulSoup(deck, features='html.parser')
    soup = soup.find('table', class_='deck-view-deck-table')
    soup = soup.find_all('tr', recursive=False)

    current_tag = None
    for row in soup:
        if 'deck-category-header' in row.attrs.get('class', []):
            category = row.text.lower()
            current_tag = next((tag for tag in ['commander', 'companion'] if tag in category), None)
        else:
            yield Card(
                row.a.string.strip(),
                row.td.string.strip(),
                re.search(
                    r'\[(.*?)\]',
                    row.a.attrs.get('data-card-id'),
                ).group(1).lower(),
                tags=[current_tag],
            )
