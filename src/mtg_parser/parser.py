#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .gramar import LINE


__all__ = [
    'parse_deck',
]


def _collapse_comments(lines):
    last_comment = None
    for line in lines:
        if 'comment' in line:
            last_comment = line['comment']
        else:
            if last_comment:
                line.setdefault('tags', []).append(last_comment)
            yield line


def _cleanup_tags(line):
    if 'tags' in line:
        line['tags'] = list(sorted(set(line['tags'])))
    return line


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


def parse_deck(decklist):
    lines = decklist.splitlines()
    lines = map(str.strip, lines)
    lines = filter(len, lines)
    lines = map(LINE.parseString, lines)
    lines = map(lambda line: line.asDict(), lines)
    lines = _collapse_comments(lines)
    lines = map(_cleanup_tags, lines)
    lines = map(_add_scryfall_url, lines)

    return lines
