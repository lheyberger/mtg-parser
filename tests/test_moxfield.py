#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser
from .utils import mock_response, assert_deck_is_valid


@pytest.mark.parametrize('src, pattern, response', [
    [
        'https://www.moxfield.com/decks/Agzx8zsi5UezWBUX5hMJPQ',
        r'https://.*?moxfield.com',
        'mock_moxfield_Agzx8zsi5UezWBUX5hMJPQ',
    ],
])
def test_parse_deck(requests_mock, src, pattern, response):
    mock_response(requests_mock, pattern, response)

    result = mtg_parser.moxfield.parse_deck(src)

    assert_deck_is_valid(result)


@pytest.mark.slow
@pytest.mark.parametrize('src', [
    'https://www.moxfield.com/decks/Agzx8zsi5UezWBUX5hMJPQ',
])
def test_parse_deck_no_mock(src):
    result = mtg_parser.moxfield.parse_deck(src)

    assert_deck_is_valid(result)
