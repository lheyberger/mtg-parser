#!/usr/bin/env python

import re

import httpx

from mtg_parser.card import Card
from mtg_parser.utils import build_pattern, match_pattern


__all__ = []


_PATTERN = build_pattern(
    'tcgplayer.com',
    r'/(content/)?magic-the-gathering/deck/(?P<deck_name>.+)/(?P<deck_id>\d+)/?',
)


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
    deck_id = re.search(_PATTERN, src).group('deck_id')
    url = f'https://infinite-api.tcgplayer.com/deck/magic/{deck_id}/?subDecks=true&cards=true'
    response = http_client.get(url)
    return response.json()


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
