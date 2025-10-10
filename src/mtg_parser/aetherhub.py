#!/usr/bin/env python

from bs4 import BeautifulSoup
from collections.abc import Iterable
from mtg_parser.card import Card
from mtg_parser.deck_parser import OnlineDeckParser
from mtg_parser.utils import build_pattern


__all__ = ['AetherhubDeckParser']


class AetherhubDeckParser(OnlineDeckParser):

    _PATTERN = build_pattern('aetherhub.com', r'/Deck/(?P<deck_id>.+)/?')

    def __init__(self):
        super().__init__(self._PATTERN)


    def _download_deck(self, src: str, http_client) -> str:
        result = http_client.get(src).text
        soup = BeautifulSoup(result, features='html.parser')
        element = soup.find(attrs={'data-deckid': True})
        deck_id = element['data-deckid']
        response = http_client.get(
            'https://aetherhub.com/Deck/FetchMtgaDeckJson',
            params={
                'deckId': deck_id,
                'langId': 0,
                'simple': False,
            },
        )
        return response.json()


    def _parse_deck(self, deck: str) -> Iterable[Card]:
        last_category = None
        for entry in deck.get('convertedDeck', []):
            quantity = entry.get('quantity')
            name = entry.get('name')
            extension = entry.get('set')
            number = entry.get('number')
            if not quantity:
                last_category = name
            elif name and quantity:
                tags = [last_category] if last_category else None
                card = Card(name, quantity, extension, number, tags)
                yield card
