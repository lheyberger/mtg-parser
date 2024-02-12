#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from collections import defaultdict

import requests
from bs4 import BeautifulSoup
from mtg_parser.card import Card


__all__ = []


def can_handle(src):
    return (
        isinstance(src, str)
        and
        re.match(r'(?:https?://)?(?:www\.)?tappedout\.net/mtg-decks/', src)
    )


def parse_deck(src, session=requests):
    deck = None
    if can_handle(src):
        deck = _parse_deck(_download_deck(src, session))
    return deck


def _download_deck(src, session):
    response = session.head(src, allow_redirects=True)
    src = response.url
    response = session.get(src, params={'cat': 'custom'})
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
            tags=tags.get(card_name, [])
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
