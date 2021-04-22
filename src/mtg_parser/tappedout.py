#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from bs4 import BeautifulSoup
from mtg_parser.decklist import parse_deck as decklist_parse_deck


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
        src.strip().startswith('https://tappedout.net/mtg-decks/')
    )


def _download_deck(src):
    result = requests.get(src)
    return result.text


def _parse_deck(deck):
    soup = BeautifulSoup(deck, features='html.parser')
    commanders = _find_cards(soup, r'^Commander')
    companions = _find_cards(soup, r'^Companion')

    cardlist = soup.find('textarea', id='mtga-textarea')
    cards = decklist_parse_deck(cardlist.get_text(strip=True))

    for card in cards:
        if card.name in commanders:
            card.tags.add('commander')
        if card.name in companions:
            card.tags.add('companion')
        yield card


def _find_cards(soup, pattern):
    header = soup.find('h3', string=re.compile(pattern))
    if not header:
        return []

    cardlist = header.find_next_sibling('ul', class_='boardlist')
    if not cardlist:
        return []

    cards = cardlist.find_all('a', class_='card-hover')
    if not cards:
        return []

    return [card['data-name'] for card in cards]
