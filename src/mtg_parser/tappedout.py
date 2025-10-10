#!/usr/bin/env python

from bs4 import BeautifulSoup
from collections import defaultdict
from collections.abc import Iterable
from re import fullmatch, sub
from mtg_parser.card import Card
from mtg_parser.deck_parser import OnlineDeckParser
from mtg_parser.utils import build_pattern


__all__ = ['TappedoutDeckParser']


class TappedoutDeckParser(OnlineDeckParser):

    _PATTERN = build_pattern('tappedout.net', r'/mtg-decks/(?P<deck_id>.+)/?')

    def __init__(self):
        super().__init__(self._PATTERN)


    def _download_deck(self, src: str, http_client) -> str:
        response = http_client.get(src, params={'cat': 'custom'})
        return response.text


    def _parse_deck(self, deck: str) -> Iterable[Card]:
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
            tag = self._format_tag(tag.text)
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


    @classmethod
    def _format_tag(cls, tag: str) -> str:
        match = fullmatch(r'(.*?)(?:\s+\(\d+\))?', tag)
        tag = match.group(1)
        tag = sub(r'[^\w\s]', '', tag)
        tag = tag.lower()
        tag = tag.split()
        tag = map(str.strip, tag)
        tag = filter(len, tag)
        tag = '_'.join(tag)
        return tag
