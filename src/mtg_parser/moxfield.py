#!/usr/bin/env python

from re import search
from collections.abc import Iterable
from mtg_parser.card import Card
from mtg_parser.deck_parser import OnlineDeckParser
from mtg_parser.utils import build_pattern


__all__ = ['MoxfieldDeckParser']


class MoxfieldDeckParser(OnlineDeckParser):

    _PATTERN = build_pattern('moxfield.com', r'/decks/(?P<deck_id>[a-zA-Z0-9-_]+)/?')

    def __init__(self):
        super().__init__(self._PATTERN)


    def _download_deck(self, src: str, http_client) -> str:
        deck_id = search(self._PATTERN, src).group('deck_id')
        url = f"https://api.moxfield.com/v2/decks/all/{deck_id}"
        response = http_client.get(url)
        return response.json()


    def _parse_deck(self, deck: str) -> Iterable[Card]:
        for key, value in deck['commanders'].items():
            yield Card(key, **self._extract_information(value), tags=['commander'])

        for key, value in deck['companions'].items():
            yield Card(key, **self._extract_information(value), tags=['companion'])

        for key, value in deck['mainboard'].items():
            yield Card(key, **self._extract_information(value))


    @classmethod
    def _extract_information(cls, card):
        return {
            'quantity': card.get('quantity', 1),
            'extension': card.get('card', {}).get('set'),
            'number': card.get('card', {}).get('cn'),
        }
