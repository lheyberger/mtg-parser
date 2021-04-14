#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mtg_parser.archidekt import can_handle as archidekt_can_handle
from mtg_parser.archidekt import parse_deck as archidekt_parse_deck

from mtg_parser.deckstats import can_handle as deckstats_can_handle
from mtg_parser.deckstats import parse_deck as deckstats_parse_deck

from mtg_parser.moxfield import can_handle as moxfield_can_handle
from mtg_parser.moxfield import parse_deck as moxfield_parse_deck

from mtg_parser.tappedout import can_handle as tappedout_can_handle
from mtg_parser.tappedout import parse_deck as tappedout_parse_deck

from mtg_parser.decklist import can_handle as decklist_can_handle
from mtg_parser.decklist import parse_deck as decklist_parse_deck


__all__ = [
    'can_handle',
    'parse_deck',
]


def can_handle(src):
    handlers = [
        archidekt_can_handle,
        deckstats_can_handle,
        moxfield_can_handle,
        tappedout_can_handle,
        decklist_can_handle,
    ]
    return any(handler(src) for handler in handlers)


def parse_deck(src):
    handlers = [
        (archidekt_can_handle, archidekt_parse_deck),
        (deckstats_can_handle, deckstats_parse_deck),
        (moxfield_can_handle, moxfield_parse_deck),
        (tappedout_can_handle, tappedout_parse_deck),
        (decklist_can_handle, decklist_parse_deck),
    ]
    for _can_handle, _parse_deck in handlers:
        if _can_handle(src):
            return _parse_deck(src)
    return None
