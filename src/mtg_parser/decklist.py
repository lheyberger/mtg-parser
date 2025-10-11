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
        return isinstance(src, str) and next(self._parse_deck(src), None)


    def parse_deck(self, src: str, *args: Any, **kwargs: Any) -> Optional[Iterable[Card]]:
        del args, kwargs

        if not self.can_handle(src):
            return None

        return self._parse_deck(src)


    @classmethod
    def _parse_deck(cls, deck: str) -> Iterable[Card]:
        lines = deck.splitlines()
        lines = map(str.strip, lines)
        lines = filter(len, lines)
        lines = map(parse_line, lines)
        lines = filter(bool, lines)
        lines = map(lambda line: line.asDict(), lines)
        lines = cls._collapse_comments(lines)
        lines = map(cls._to_card, lines)
        return lines


    @classmethod
    def _collapse_comments(cls, lines):
        last_comment = None
        for line in lines:
            if 'comment' in line:
                last_comment = line['comment']
            else:
                if last_comment:
                    line.setdefault('tags', []).append(last_comment)
                yield line


    @classmethod
    def _to_card(cls, line: str) -> Card:
        return Card(
            line.get('card_name'),
            line.get('quantity'),
            line.get('extension'),
            line.get('collector_number'),
            line.get('tags'),
        )
