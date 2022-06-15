#!/usr/bin/env python
# -*- coding: utf-8 -*-

from operator import methodcaller
import requests
import mtg_parser.aetherhub
import mtg_parser.archidekt
import mtg_parser.deckstats
import mtg_parser.moxfield
import mtg_parser.mtggoldfish
import mtg_parser.mtgjson
import mtg_parser.scryfall
import mtg_parser.tappedout
import mtg_parser.tcgplayer
import mtg_parser.decklist


__all__ = [
    'can_handle',
    'parse_deck',
]


_PARSERS = [
    mtg_parser.aetherhub,
    mtg_parser.archidekt,
    mtg_parser.deckstats,
    mtg_parser.moxfield,
    mtg_parser.mtggoldfish,
    mtg_parser.mtgjson,
    mtg_parser.scryfall,
    mtg_parser.tappedout,
    mtg_parser.tcgplayer,
    mtg_parser.decklist,
]


def can_handle(src):
    return any(map(methodcaller('can_handle', src), _PARSERS))


def parse_deck(src, session=requests):
    for parser in _PARSERS:
        if parser.can_handle(src):
            deck = parser.parse_deck(src, session)
            if deck:
                return deck
    return None
