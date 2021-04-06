#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = [
    'diff',
]


def diff(deck1, deck2, differences_only=False):
    deckset1 = set(c['card_name'] for c in deck1)
    deckset2 = set(c['card_name'] for c in deck2)

    result = {}
    result['deck1 - deck2'] = deckset1.difference(deckset2)
    if not differences_only:
        result['deck1 x deck2'] = deckset1.intersection(deckset2)
    result['deck2 - deck1'] = deckset2.difference(deckset1)
    return result
