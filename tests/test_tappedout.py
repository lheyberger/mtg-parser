#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser
from .utils import mock_response


@pytest.mark.parametrize('src, pattern, response', [
    [
        'https://tappedout.net/mtg-decks/mtg-parser-3-amigos/',
        r'https://tappedout.net/',
        'mock_tappedout_3-amigos',
    ],
])
def test_parse_deck(requests_mock, src, pattern, response):
    mock_response(requests_mock, pattern, response)

    result = mtg_parser.tappedout.parse_deck(src)
    result = list(result)

    assert result and all(result)


@pytest.mark.slow
@pytest.mark.parametrize('src', [
    'https://tappedout.net/mtg-decks/mtg-parser-3-amigos/',
])
def test_parse_deck_no_mock(src):
    result = mtg_parser.tappedout.parse_deck(src)
    result = list(result)

    assert result and all(result)
