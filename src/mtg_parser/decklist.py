#!/usr/bin/env python

from mtg_parser.card import Card
from mtg_parser.grammar import parse_line


__all__ = []


def can_handle(src):
    return (
        isinstance(src, str)
        and
        next(_parse_deck(src), None)
    )


def parse_deck(src, *args, **kwargs):
    del args, kwargs
    deck = None
    if can_handle(src):
        deck = _parse_deck(src)
    return deck


def _parse_deck(deck):
    lines = deck.splitlines()
    lines = map(str.strip, lines)
    lines = filter(len, lines)
    lines = map(parse_line, lines)
    lines = filter(bool, lines)
    lines = map(lambda line: line.asDict(), lines)
    lines = _collapse_comments(lines)
    lines = map(_to_card, lines)
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


def _to_card(line):
    return Card(
        line.get('card_name'),
        line.get('quantity'),
        line.get('extension'),
        line.get('collector_number'),
        line.get('tags'),
    )
