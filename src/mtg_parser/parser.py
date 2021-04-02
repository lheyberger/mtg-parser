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


def parse_deck(deckstring):
    lines = filter(len, map(str.strip, deckstring.splitlines()))
    lines = map(LINE.parseString, lines)
    lines = map(lambda line: line.asDict(), lines)
    lines = _collapse_comments(lines)
    lines = map(_cleanup_tags, lines)

    return lines
