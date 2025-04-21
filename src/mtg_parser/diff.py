#!/usr/bin/env python

__all__ = [
    'diff',
]


def _format_name(card_name):
    return card_name.split('//')[0].strip()


def diff(deck1, deck2, differences_only=False):
    deckset1 = set(_format_name(card.name) for card in deck1)
    deckset2 = set(_format_name(card.name) for card in deck2)

    result = {}
    result['deck1 - deck2'] = deckset1.difference(deckset2)
    if not differences_only:
        result['deck1 x deck2'] = deckset1.intersection(deckset2)
    result['deck2 - deck1'] = deckset2.difference(deckset1)
    return result
