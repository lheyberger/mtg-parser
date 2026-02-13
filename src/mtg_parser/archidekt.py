#!/usr/bin/env python

from re import search
from collections.abc import Iterable
from typing import Any, Optional
from mtg_parser.card import Card
from mtg_parser.deck_parser import OnlineDeckParser
from mtg_parser.utils import build_pattern


__all__ = ['ArchidektDeckParser']


class ArchidektDeckParser(OnlineDeckParser[dict]):

    _PATTERN = build_pattern('archidekt.com', r'/decks/(?P<deck_id>\d+)/?')

    def __init__(self):
        super().__init__(self._PATTERN)


    def _download_deck(self, src: str, http_client: Any) -> Optional[dict]:
        match = search(self._PATTERN, src)
        deck_id = match.group('deck_id') if match else None
        if not deck_id:
            return None # pragma: no cover
        url = f"https://archidekt.com/api/decks/{deck_id}/"
        response = http_client.get(url)
        return response.json()


    def _parse_deck(self, deck: dict) -> Iterable[Card]:
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
