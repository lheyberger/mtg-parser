#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser
from .utils import mock_response, assert_deck_is_valid


@pytest.mark.parametrize('src, pattern, response', [
    [
        'https://mtgjson.com/api/v5/decks/BreedLethality_CM2.json',
        r'(https?://)?(www\.)?mtgjson\.com',
        'mock_mtgjson_breedlethality_cmd2.json',
    ],
])
def test_parse_deck(requests_mock, src, pattern, response):
    mock_response(requests_mock, pattern, response)

    result = mtg_parser.mtgjson.parse_deck(src)

    assert_deck_is_valid(result)


@pytest.mark.slow
@pytest.mark.parametrize('src', [
    'https://mtgjson.com/api/v5/decks/BreedLethality_CM2.json',
])
def test_parse_deck_no_mock(src):
    result = mtg_parser.mtgjson.parse_deck(src)

    assert_deck_is_valid(result)
