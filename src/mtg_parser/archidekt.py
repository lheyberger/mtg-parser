#!/usr/bin/env python

from re import search
from collections.abc import Iterable
from mtg_parser.card import Card
from mtg_parser.deck_parser import OnlineDeckParser
from mtg_parser.utils import build_pattern


__all__ = ['ArchidektDeckParser']


class ArchidektDeckParser(OnlineDeckParser):

    _PATTERN = build_pattern('archidekt.com', r'/decks/(?P<deck_id>\d+)/?')

    def __init__(self):
        super().__init__(self._PATTERN)


    def _download_deck(self, src: str, http_client) -> str:
        deck_id = search(self._PATTERN, src).group('deck_id')
        url = f"https://archidekt.com/api/decks/{deck_id}/"
        response = http_client.get(url)
        return response.json()


    def _parse_deck(self, deck: str) -> Iterable[Card]:
        categories = deck['categories']
        categories = filter(lambda c: c.get('includedInDeck', False), categories)
        categories = map(lambda c: c['name'], categories)
        categories = set(categories)
        for card in deck['cards']:
            if not card['categories'] or categories & set(card['categories']):
                yield Card(
                    card['card']['oracleCard']['name'],
                    card['quantity'],
                    card['card']['edition']['editioncode'],
                    card['card'].get('collectorNumber'),
                    card['categories'],
                )
