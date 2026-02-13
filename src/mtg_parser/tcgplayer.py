#!/usr/bin/env python

from re import search
from typing import Any, Optional
from collections.abc import Iterable
from mtg_parser.card import Card
from mtg_parser.deck_parser import OnlineDeckParser
from mtg_parser.utils import build_pattern


__all__ = ['TcgplayerDeckParser']


class TcgplayerDeckParser(OnlineDeckParser[dict]):

    _PATTERN = build_pattern(
        'tcgplayer.com',
        r'/(content/)?magic-the-gathering/deck/(?P<deck_name>.+)/(?P<deck_id>\d+)/?',
    )

    def __init__(self):
        super().__init__(self._PATTERN)


    def _download_deck(self, src: str, http_client: Any) -> Optional[dict]:
        match = search(self._PATTERN, src)
        deck_id = match.group('deck_id') if match else None
        if not deck_id:
            return None # pragma: no cover
        url = f'https://infinite-api.tcgplayer.com/deck/magic/{deck_id}/?subDecks=true&cards=true'
        response = http_client.get(url)
        return response.json()


    def _parse_deck(self, deck: dict) -> Optional[Iterable[Card]]:
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
