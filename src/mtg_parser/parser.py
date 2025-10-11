#!/usr/bin/env python

from collections.abc import Iterable
from operator import methodcaller
from mtg_parser.deck_parser import BaseParser
from mtg_parser.card import Card
from mtg_parser.aetherhub import AetherhubDeckParser
from mtg_parser.archidekt import ArchidektDeckParser
from mtg_parser.decklist import DecklistDeckParser
from mtg_parser.deckstats import DeckstatsDeckParser
from mtg_parser.moxfield import MoxfieldDeckParser
from mtg_parser.mtggoldfish import MtggoldfishDeckParser
from mtg_parser.mtgjson import MtgjsonDeckParser
from mtg_parser.scryfall import ScryfallDeckParser
from mtg_parser.tappedout import TappedoutDeckParser
from mtg_parser.tcgplayer import TcgplayerDeckParser


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
