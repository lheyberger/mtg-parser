#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser
from .utils import mock_response


@pytest.mark.parametrize('src, pattern, response', [
    [
        'https://deckstats.net/decks/30198/2034245--mtg-parser-3-amigos',
        r'https://deckstats.net/',
        'mock_deckstats_30198_2034245',
    ],
])
def test_parse_deck(requests_mock, src, pattern, response):
    mock_response(requests_mock, pattern, response)

    result = mtg_parser.deckstats.parse_deck(src)
    result = list(result)

    assert result and all(result)


@pytest.mark.slow
@pytest.mark.parametrize('src', [
    'https://deckstats.net/decks/30198/2034245--mtg-parser-3-amigos',
])
def test_parse_deck_no_mock(src):
    result = mtg_parser.deckstats.parse_deck(src)
    result = list(result)

    assert result and all(result)
