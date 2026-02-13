#!/usr/bin/env python

from collections.abc import Iterable
from typing import Any, Optional
from mtg_parser.card import Card
from mtg_parser.deck_parser import OnlineDeckParser
from mtg_parser.utils import build_pattern


__all__ = ['MtgjsonDeckParser']


class MtgjsonDeckParser(OnlineDeckParser[dict]):

    _PATTERN = build_pattern('mtgjson.com', r'/api/v5/decks/(?P<deck_id>.+\.json)')

    def __init__(self):
        super().__init__(self._PATTERN)


    def _download_deck(self, src: str, http_client: Any) -> Optional[dict]:
        response = http_client.get(src)
        return response.json()


    def _parse_deck(self, deck: dict) -> Optional[Iterable[Card]]:
        for card in deck.get('data', {}).get('commander', []):
            yield Card(
                card['name'],
                quantity=card['count'],
                extension=card['setCode'],
                tags=['commander'],
            )

        for card in deck.get('data', {}).get('mainBoard', []):
            yield Card(
                card['name'],
                quantity=card['count'],
                extension=card['setCode'],
            )
