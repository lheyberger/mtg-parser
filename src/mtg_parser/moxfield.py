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
        response.raise_for_status()
        return response.json()


    def _parse_deck(self, deck: dict) -> Optional[Iterable[Card]]:
        for card in self._iterate_cards(deck.get('commanders', [])):
            yield Card(**self._extract_information(card), tags=['commander'])

        for card in self._iterate_cards(deck.get('companions', [])):
            yield Card(**self._extract_information(card), tags=['companion'])

        for card in self._iterate_cards(deck.get('mainboard', [])):
            yield Card(**self._extract_information(card))


    @classmethod
    def _iterate_cards(cls, card_list: dict) -> dict:
        for card in card_list.values():
            if 'printingData' in card:
                yield from card['printingData']
            else:
                yield card

        for key, value in deck['sideboard'].items():
            yield Card(key, **self._extract_information(value), tags=['sideboard'])


    @classmethod
    def _extract_information(cls, card) -> dict:
        return {
            'name': card.get('card', {}).get('name'),
            'quantity': card.get('quantity', 1),
            'extension': card.get('card', {}).get('set'),
            'number': card.get('card', {}).get('cn'),
        }
