#!/usr/bin/env python

import re
from collections import defaultdict

import httpx
from bs4 import BeautifulSoup

from mtg_parser.card import Card
from mtg_parser.utils import build_pattern, match_pattern


__all__ = []


_PATTERN = build_pattern('tappedout.net', r'/mtg-decks/(?P<deck_id>.+)/?')


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
    response = http_client.get(src, params={'cat': 'custom'})
    return response.text


def _parse_deck(deck):
    soup = BeautifulSoup(deck, features='html.parser')
    board_container = soup.find('div', class_='board-container')

    quantities = {}
    for card in board_container.find_all('a', class_="qty board", attrs={
        'data-name': True,
        'data-qty': True,
    }):
        quantities[card['data-name']] = card['data-qty']

    tags = defaultdict(set)
    for card in board_container.find_all('a', class_='card-hover', attrs={
        'data-name': True,
        'data-url': True,
    }):
        tag = card.find_previous('h3')
        tag = _format_tag(tag.text)
        if tag in ('commander', 'commanders'):
            tag = 'commander'
        elif tag in ('companion', 'companions'):
            tag = 'companion'
        else:
            tag = None
        tags[card['data-name']].add(tag)

    for card_name in sorted(set(quantities.keys()) | set(tags.keys())):
        yield Card(
            card_name,
            quantity=quantities.get(card_name, 1),
            tags=tags.get(card_name, []),
        )


def _format_tag(tag):
    match = re.fullmatch(r'(.*?)(?:\s+\(\d+\))?', tag)
    tag = match.group(1)
    tag = re.sub(r'[^\w\s]', '', tag)
    tag = tag.lower()
    tag = tag.split()
    tag = map(str.strip, tag)
    tag = filter(len, tag)
    tag = '_'.join(tag)
    return tag
