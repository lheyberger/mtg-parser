#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mtg_parser.aetherhub
import mtg_parser.archidekt
import mtg_parser.deckstats
import mtg_parser.moxfield
import mtg_parser.mtggoldfish
import mtg_parser.scryfall
import mtg_parser.tappedout
import mtg_parser.tcgplayer
import mtg_parser.decklist


__all__ = [
    'parse_deck',
]


def parse_deck(src):
    parsers = [
        mtg_parser.aetherhub,
        mtg_parser.archidekt,
        mtg_parser.deckstats,
        mtg_parser.moxfield,
        mtg_parser.mtggoldfish,
        mtg_parser.scryfall,
        mtg_parser.tappedout,
        mtg_parser.tcgplayer,
        mtg_parser.decklist,
    ]
    for parser in parsers:
        if parser.can_handle(src):
            deck = parser.parse_deck(src)
            if deck:
                return deck
    return None
