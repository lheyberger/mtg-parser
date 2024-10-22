#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
from mtg_parser.card import Card
from mtg_parser.utils import build_pattern, match_pattern


__all__ = []


_PATTERN = build_pattern(
    'infinite.tcgplayer.com',
    r'/magic-the-gathering/deck/(?P<deck_name>.+)/(?P<deck_id>\d+)/?',
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
    url = f'https://infinite-api.tcgplayer.com/deck/magic/{deck_id}/?subDecks=true&cards=true'
    headers = {}
    if 'User-Agent' not in getattr(session, 'headers', {}):
        headers['User-Agent'] = ' '.join([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
            'AppleWebKit/537.36 (KHTML, like Gecko)',
            'Chrome/129.0.0.0 Safari/537.3',
        ])
    return session.get(url, headers=headers).json()


def _parse_deck(deck):
    subdecks = deck.get('result', {}).get('deck', {}).get('subDecks', {})
    all_cards = deck.get('result', {}).get('cards', {})

    for card in subdecks.get('commandzone', []):
        card_detail = all_cards.get(str(card['cardID']), {})
        yield Card(card_detail['name'], card['quantity'], card_detail['set'], tags=['commander'])

    for card in subdecks.get('sideboard', []):
        card_detail = all_cards.get(str(card['cardID']), {})
        yield Card(card_detail['name'], card['quantity'], card_detail['set'], tags=['companion'])

    for card in subdecks.get('maindeck', []):
        card_detail = all_cards.get(str(card['cardID']), {})
        yield Card(card_detail['name'], card['quantity'], card_detail['set'])
