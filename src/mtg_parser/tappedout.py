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
    skipped_list = ['sideboard', ]
    board_container = soup.find('div', class_='board-container')
    boardlists = board_container.find_all('ul', class_='boardlist')
    for boardlist in boardlists:
        tag = boardlist.find_previous_sibling('h3')
        tag = _format_tag(tag.text)
        if any(tag.startswith(skipped_tag) for skipped_tag in skipped_list):
            continue
        if tag in ('commander', 'commanders'):
            tag = 'commander'
        quantities = boardlist.find_all('a', class_="qty board")
        quantities = {
            elem['data-name']: elem['data-qty']
            for elem in quantities
        }
        cards = boardlist.find_all(
            'a',
            attrs={
                'data-url': True,
                'data-name': True,
            }
        )
        for card in cards:
            yield Card(
                card['data-name'],
                quantity=quantities.get(card['data-name'], 1),
                tags=[tag],
            )


def _format_tag(tag):
    tag = re.fullmatch(r'(.*?)\s\(\d+\)', tag).group(1)
    tag = re.sub(r'[^\w\s]', '', tag)
    tag = tag.lower()
    tag = tag.split()
    tag = map(str.strip, tag)
    tag = filter(len, tag)
    tag = '_'.join(tag)
    return tag
