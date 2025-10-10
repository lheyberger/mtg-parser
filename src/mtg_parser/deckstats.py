#!/usr/bin/env python

from json import loads
from collections.abc import Iterable
from mtg_parser.card import Card
from mtg_parser.deck_parser import OnlineDeckParser
from mtg_parser.utils import build_pattern


__all__ = ['DeckstatsDeckParser']


class DeckstatsDeckParser(OnlineDeckParser):

    _PATTERN = build_pattern('deckstats.net', r'/decks/(?P<user_id>\d+)/(?P<deck_id>\d+-.*)/?')

    def __init__(self):
        super().__init__(self._PATTERN)


    def _download_deck(self, src: str, http_client) -> str:
        start_token = 'init_deck_data(' # noqa: S105
        end_token = ');' # noqa: S105

        result = http_client.get(src).text.splitlines()
        result = next(line for line in result if start_token in line)

        result = result[result.find(start_token) + len(start_token):]
        result = result[:result.find(end_token)]

        _i = 0
        opened = 0
        for _i, char in enumerate(result):
            if char == '{':
                opened = opened + 1
            if char == '}':
                opened = opened - 1
            if opened <= 0:
                break
        result = result[:_i+1]
        return loads(result)


    def _parse_deck(self, deck: str) -> Iterable[Card]:
        for section in deck.get('sections', []):
            for card in section.get('cards', {}):
                yield Card(
                    card['name'],
                    card['amount'],
                    tags=self._get_tags(card),
                )


    @classmethod
    def _get_tags(cls, card) -> Iterable[str]:
        if card.get('isCommander', False):
            yield 'commander'
        if card.get('isCompanion', False):
            yield 'companion'
