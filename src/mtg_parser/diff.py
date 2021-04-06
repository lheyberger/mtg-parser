#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .parser import parse_deck


__all__ = [
    'diff',
]


def diff(decklist1, decklist2):
    deck1 = parse_deck(decklist1)
    deck2 = parse_deck(decklist2)

    deckset1 = set(c['card_name'] for c in deck1)
    deckset2 = set(c['card_name'] for c in deck2)

    return {
        'decklist1 - decklist2': deckset1.difference(deckset2),
        'decklist1 x decklist2': deckset1.intersection(deckset2),
        'decklist2 - decklist1': deckset2.difference(deckset1),
    }
