#!/usr/bin/env python

from bs4 import BeautifulSoup
from json import loads
from collections.abc import Iterable
from typing import Any, Optional
from mtg_parser.card import Card
from mtg_parser.deck_parser import OnlineDeckParser
from mtg_parser.utils import build_pattern


__all__ = ['DeckstatsDeckParser']


class DeckstatsDeckParser(OnlineDeckParser[dict]):

    _PATTERN = build_pattern('deckstats.net', r'/decks/(?P<user_id>\d+)/(?P<deck_id>\d+-.*)/?')

    def __init__(self):
        super().__init__(self._PATTERN)


    def _download_deck(self, src: str, http_client: Any) -> dict:
        result = http_client.get(src).text
        soup = BeautifulSoup(result, features='html.parser')
        script_tag = soup.find('script', attrs={'data-page': 'app', 'type': 'application/json'})
        data = loads(script_tag.string)
        return data


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
