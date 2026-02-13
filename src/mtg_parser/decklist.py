#!/usr/bin/env python

from collections.abc import Iterable
from typing import Any, Optional
from mtg_parser.card import Card
from mtg_parser.deck_parser import BaseParser
from mtg_parser.grammar import parse_line


__all__ = ['DecklistDeckParser']


class DecklistDeckParser(BaseParser):

    def __init__(self) -> None:
        super().__init__()


    def can_handle(self, src: str) -> bool:
        if not isinstance(src, str):
            return False
        deck_iterator = self._parse_deck(src)
        return next(iter(deck_iterator), None) is not None if deck_iterator else False


    def parse_deck(self, src: str, *args: Any, **kwargs: Any) -> Optional[Iterable[Card]]:
        del args, kwargs

        if not self.can_handle(src):
            return None

        return self._parse_deck(src)


    @classmethod
    def _parse_deck(cls, deck: str) -> Optional[Iterable[Card]]:
        lines = deck.splitlines()
        lines = map(str.strip, lines)
        lines = filter(len, lines)
        lines = map(parse_line, lines)
        lines = filter(bool, lines)
        lines = map(lambda line: line.asDict(), lines)
        return cls._collapse_comments(lines)


    @classmethod
    def _collapse_comments(cls, lines: Iterable[dict[str, Any]]) -> Iterable[Card]:
        last_comment = None
        for line in lines:
            if 'comment' in line:
                last_comment = line['comment']
            else:
                if last_comment:
                    line.setdefault('tags', []).append(last_comment)
                yield Card(
                    line.get('card_name', 'InvalidCard'),
                    line.get('quantity', 1),
                    line.get('extension'),
                    line.get('collector_number'),
                    line.get('tags'),
                )
