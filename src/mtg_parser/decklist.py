#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mtg_parser.grammar import parse_line
from mtg_parser.utils import get_scryfall_url


__all__ = []


def parse_deck(src):
    deck = None
    if _can_handle(src):
        deck = _parse_deck(src)
    return deck


def _can_handle(src):
    return isinstance(src, str)


def _parse_deck(deck):
    lines = deck.splitlines()
    lines = map(str.strip, lines)
    lines = filter(len, lines)
    lines = map(parse_line, lines)
    lines = filter(bool, lines)
    lines = map(lambda line: line.asDict(), lines)
    lines = _collapse_comments(lines)
    lines = map(_cleanup_tags, lines)
    lines = map(_add_scryfall_url, lines)
    return lines


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
    line['scryfall_url'] = get_scryfall_url(
        line.get('card_name'),
        line.get('extension'),
        line.get('collector_number'),
    )
    return line
