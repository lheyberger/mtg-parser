#!/usr/bin/env python

from re import search
from collections.abc import Iterable
from typing import Any, Optional
from mtg_parser.card import Card
from mtg_parser.deck_parser import OnlineDeckParser
from mtg_parser.utils import build_pattern


__all__ = ['MoxfieldDeckParser']


class MoxfieldDeckParser(OnlineDeckParser[dict]):

    _PATTERN = build_pattern('moxfield.com', r'/decks/(?P<deck_id>[a-zA-Z0-9-_]+)/?')

    def __init__(self):
        super().__init__(self._PATTERN)


    def _download_deck(self, src: str, http_client: Any) -> Optional[dict]:
        match = search(self._PATTERN, src)
        deck_id = match.group('deck_id') if match else None
        if not deck_id:
            return None # pragma: no cover
        url = f"https://api.moxfield.com/v2/decks/all/{deck_id}"
        response = http_client.get(url)
        return response.json()


    def _parse_deck(self, deck: dict) -> Optional[Iterable[Card]]:
        for key, value in deck['commanders'].items():
            yield Card(key, **self._extract_information(value), tags=['commander'])

        for key, value in deck['companions'].items():
            yield Card(key, **self._extract_information(value), tags=['companion'])

        for key, value in deck['mainboard'].items():
            yield Card(key, **self._extract_information(value))


    @classmethod
    def _extract_information(cls, card) -> dict:
        return {
            'quantity': card.get('quantity', 1),
            'extension': card.get('card', {}).get('set'),
            'number': card.get('card', {}).get('cn'),
        }
