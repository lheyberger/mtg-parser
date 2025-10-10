#!/usr/bin/env python

from collections.abc import Iterable
from csv import DictReader
from io import StringIO
from re import search
from mtg_parser.card import Card
from mtg_parser.deck_parser import OnlineDeckParser
from mtg_parser.utils import build_pattern


__all__ = ['ScryfallDeckParser']


class ScryfallDeckParser(OnlineDeckParser):

    _PATTERN = build_pattern(
        'scryfall.com',
        r'/(?P<user_id>@.+)/decks/(?P<deck_id>\w{8}-\w{4}-\w{4}-\w{4}-\w{12})/?',
    )

    def __init__(self):
        super().__init__(self._PATTERN)


    def _download_deck(self, src: str, http_client) -> str:
        deck_id = search(self._PATTERN, src).group('deck_id')
        url = f"https://api.scryfall.com/decks/{deck_id}/export/csv"
        response = http_client.get(url)
        return response.text


    def _parse_deck(self, deck: str) -> Iterable[Card]:
        deck_csv = StringIO(deck)
        reader = DictReader(deck_csv)
        for card in reader:
            yield Card(
                card['name'],
                int(card['count']),
                card['set_code'],
                card['collector_number'],
                tags=self._get_tags(card['section']),
            )


    @classmethod
    def _get_tags(cls, section_name: str) -> Iterable[str]:
        if section_name and section_name.lower() == 'commanders':
            yield 'commander'
        if section_name and section_name.lower() == 'outside':
            yield 'companion'
