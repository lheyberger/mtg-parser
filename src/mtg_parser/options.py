#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = [
    'add_scryfall_urls',
]


def _add_scryfall_url(line):
    if 'extension' in line and 'collector_number' in line:
        line['scryfall_url'] = 'https://api.scryfall.com/cards/{}/{}'.format(
            line['extension'].lower(),
            line['collector_number'].lower(),
        )
    elif 'card_name' in line:
        card_name = line['card_name'].split()
        card_name = map(str.strip, card_name)
        card_name = filter(len, card_name)
        card_name = '+'.join(card_name)
        line['scryfall_url'] = (
            'https://api.scryfall.com/cards/named?fuzzy=' + card_name
        )
    return line


def add_scryfall_urls(lines):
    return map(_add_scryfall_url, lines)
