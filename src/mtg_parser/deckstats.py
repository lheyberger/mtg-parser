#!/usr/bin/env python

from collections.abc import Iterable
from json import loads
from typing import Any, Optional
from selectolax.lexbor import LexborHTMLParser
from mtg_parser.card import Card
from mtg_parser.deck_parser import OnlineDeckParser
from mtg_parser.utils import build_pattern


__all__ = ['DeckstatsDeckParser']


class DeckstatsDeckParser(OnlineDeckParser[dict]):

    _PATTERN = build_pattern('deckstats.net', r'/decks/(?P<user_id>\d+)/(?P<deck_id>\d+-.*)/?')

    def __init__(self):
        super().__init__(self._PATTERN)


    def _download_deck(self, src: str, http_client: Any) -> Optional[dict]:
        response = http_client.get(src)
        response.raise_for_status()
        tree = LexborHTMLParser(response.text)
        script_tag = tree.css_first('script[data-page="app"][type="application/json"]')
        return loads(script_tag.text())


    def _parse_deck(self, deck: dict) -> Optional[Iterable[Card]]:
        for card in deck.get('props', {}).get('entries', []):
            yield Card(
                card['name'],
                card['amount'],
                tags=self._get_tags(card),
            )


    @classmethod
    def _get_tags(cls, card) -> Iterable[str]:
        if card.get('is_commander', False):
            yield 'commander'
        if card.get('comment') == '!Companion':
            yield 'companion'
