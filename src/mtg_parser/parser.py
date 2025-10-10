#!/usr/bin/env python

from collections.abc import Iterable
from operator import methodcaller
from .deck_parser import BaseParser
from .card import Card
from .aetherhub import AetherhubDeckParser
from .archidekt import ArchidektDeckParser
from .decklist import DecklistDeckParser
from .deckstats import DeckstatsDeckParser
from .moxfield import MoxfieldDeckParser
from .mtggoldfish import MtggoldfishDeckParser
from .mtgjson import MtgjsonDeckParser
from .scryfall import ScryfallDeckParser
from .tappedout import TappedoutDeckParser
from .tcgplayer import TcgplayerDeckParser


__all__ = ['can_handle', 'parse_deck', 'DeckParser']


def can_handle(src: str) -> bool:
    parser = DeckParser()
    return parser.can_handle(src)


def parse_deck(src, http_client=None):
    parser = DeckParser()
    return parser.parse_deck(src, http_client)


class DeckParser(BaseParser):

    _PARSERS = [
        AetherhubDeckParser(),
        ArchidektDeckParser(),
        DeckstatsDeckParser(),
        MoxfieldDeckParser(),
        MtggoldfishDeckParser(),
        MtgjsonDeckParser(),
        ScryfallDeckParser(),
        TappedoutDeckParser(),
        TcgplayerDeckParser(),
        DecklistDeckParser(),
    ]

    def can_handle(self, src: str) -> bool:
        return any(map(methodcaller('can_handle', src), self._PARSERS))


    def parse_deck(self, src: str, http_client=None) -> Iterable[Card]:
        for parser in self._PARSERS:
            if parser.can_handle(src):
                deck = parser.parse_deck(src, http_client)
                if deck:
                    return deck
        return None
