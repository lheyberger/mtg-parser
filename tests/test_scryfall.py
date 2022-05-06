#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser
from .utils import mock_response, assert_deck_is_valid


@pytest.mark.parametrize('src, pattern, response', [
    [
        'https://scryfall.com/@gorila/decks/e7aceb4c-29d5-49f5-9a49-c24f64da264b',
        r'(https?://)?(www\.)?scryfall\.com',
        'mock_scryfall_e7aceb4c-29d5-49f5-9a49-c24f64da264b',
    ],
])
def test_parse_deck(requests_mock, src, pattern, response):
    mock_response(requests_mock, pattern, response)

    result = mtg_parser.scryfall.parse_deck(src)

    assert_deck_is_valid(result)


@pytest.mark.slow
@pytest.mark.parametrize('src', [
    'https://scryfall.com/@gorila/decks/e7aceb4c-29d5-49f5-9a49-c24f64da264b',
])
def test_parse_deck_no_mock(src):
    result = mtg_parser.scryfall.parse_deck(src)

    assert_deck_is_valid(result)
