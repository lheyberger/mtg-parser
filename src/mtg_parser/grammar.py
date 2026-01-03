#!/usr/bin/env python

from pyparsing import (
    Literal,
    OneOrMore,
    Optional,
    ParseException,
    StringEnd,
    StringStart,
    Word,
    ZeroOrMore,
    alphanums,
    nums,
    pyparsing_unicode,
)


__all__ = ['parse_line']


QUANTITY = (
    Word(nums)
    .set_parse_action(lambda tokens: int(tokens[0]))
    .set_results_name('quantity')
)
COLLECTOR_NUMBER = (
    Word(alphanums)
    .set_results_name('collector_number')
)
EXTENSION = (
    Word(alphanums)
    .set_results_name('extension')
)
CARD_NAME = (
    OneOrMore(Word(pyparsing_unicode.alphanums + "-,/'\""))
    .set_parse_action(' '.join)
    .set_results_name('card_name')
)
TAG = (
    Literal('#').suppress() +
    Optional(Literal('!')).suppress() +
    OneOrMore(Word(pyparsing_unicode.alphanums + "-_"))
    .set_parse_action(' '.join)
    .set_results_name('tags', list_all_matches=True)
)
MTGA_EXTENSION = (
    Literal('(').suppress() + EXTENSION + Literal(')').suppress()
)
MTGA_LINE = (
    QUANTITY + CARD_NAME + MTGA_EXTENSION + COLLECTOR_NUMBER + ZeroOrMore(TAG)
)
MTGO_LINE = (
    QUANTITY + CARD_NAME + ZeroOrMore(TAG)
)
COMMENT_LINE = (
    StringStart()
    + (Literal('//!') | Literal('//') | Literal('#'))
    .suppress()
    + OneOrMore(Word(pyparsing_unicode.alphanums + "-_"))
    .set_parse_action(' '.join)
    .set_results_name('comment')
    + StringEnd()
)
LINE = (
    COMMENT_LINE | MTGA_LINE | MTGO_LINE
)


def parse_line(line):
    try:
        return LINE.parse_string(line)
    except ParseException:
        return None
