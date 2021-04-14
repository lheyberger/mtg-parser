#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mtg_parser.gramar import LINE
from mtg_parser.utils import scryfal_url_from_name, scryfal_url_from_extension


__all__ = []


def can_handle(src):
    return isinstance(src, str)


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
        line['scryfall_url'] = scryfal_url_from_extension(
            line['extension'],
            line['collector_number'],
        )
    elif 'card_name' in line:
        line['scryfall_url'] = scryfal_url_from_name(
            line['card_name']
        )
    return line
