#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser
from .utils import mock_response


@pytest.mark.parametrize('src, pattern, response', [
    [
        'https://www.archidekt.com/decks/1365846/',
        r'https://www.archidekt.com/',
        'mock_archidekt_1365846_small',
    ],
])
def test_parse_deck(requests_mock, src, pattern, response):
    mock_response(requests_mock, pattern, response)

    result = mtg_parser.archidekt.parse_deck(src)
    result = list(result)

    assert result and all(result)


@pytest.mark.slow
@pytest.mark.parametrize('src', [
    'https://www.archidekt.com/decks/1365846/',
])
def test_parse_deck_no_mock(src):
    result = mtg_parser.archidekt.parse_deck(src)
    result = list(result)

    assert result and all(result)
