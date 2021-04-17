#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mtg_parser.archidekt import parse_deck as archidekt_parse_deck
from mtg_parser.deckstats import parse_deck as deckstats_parse_deck
from mtg_parser.moxfield import parse_deck as moxfield_parse_deck
from mtg_parser.mtggoldfish import parse_deck as mtggoldfish_parse_deck
from mtg_parser.tappedout import parse_deck as tappedout_parse_deck
from mtg_parser.decklist import parse_deck as decklist_parse_deck


__all__ = [
    'parse_deck',
]


def parse_deck(src):
    parsers = [
        archidekt_parse_deck,
        deckstats_parse_deck,
        moxfield_parse_deck,
        mtggoldfish_parse_deck,
        tappedout_parse_deck,
        decklist_parse_deck,
    ]
    for _parse_deck in parsers:
        deck = _parse_deck(src)
        if deck:
            return deck
    return None
