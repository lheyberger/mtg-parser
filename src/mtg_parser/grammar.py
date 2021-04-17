#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyparsing import ParseException
from pyparsing import nums, alphanums, pyparsing_unicode
from pyparsing import OneOrMore, Optional, ZeroOrMore
from pyparsing import Word, Literal, StringStart, StringEnd


QUANTITY = (
    Word(nums)
    .setParseAction(lambda tokens: int(tokens[0]))
    .setResultsName('quantity')
)
COLLECTOR_NUMBER = (
    Word(alphanums)
    .setResultsName('collector_number')
)
EXTENSION = (
    Word(alphanums)
    .setResultsName('extension')
)
CARD_NAME = (
    OneOrMore(Word(pyparsing_unicode.alphanums + "-,/'\""))
    .setParseAction(' '.join)
    .setResultsName('card_name')
)
TAG = (
    Literal('#').suppress() +
    Optional(Literal('!')).suppress() +
    OneOrMore(Word(pyparsing_unicode.alphanums + "-_"))
    .setParseAction(' '.join)
    .setResultsName('tags', listAllMatches=True)
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
    .setParseAction(' '.join)
    .setResultsName('comment')
    + StringEnd()
)
LINE = (
    COMMENT_LINE | MTGA_LINE | MTGO_LINE
)


def parse_line(line):
    try:
        return LINE.parseString(line)
    except ParseException:
        return None
