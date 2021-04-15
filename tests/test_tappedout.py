#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests_mock
import pytest
import mtg_parser
from .utils import mock_response


@pytest.mark.parametrize('src, pattern, response', [
    [
        'https://tappedout.net/mtg-decks/food-chain-sliver/',
        r'https://tappedout.net/',
        'mock_tappedout_food-chain-sliver',
    ],
])
def test_parse_deck(requests_mock, src, pattern, response):
    mock_response(requests_mock, pattern, response)

    result = mtg_parser.tappedout.parse_deck(src)

    assert result and all(result)


@pytest.mark.parametrize('deck', [
    """
        1 Jeweled Lotus (CMR) 319
        1 Llanowar Elves (M12) 182
    """
])
def test_internal_parse_deck(deck):
    result = mtg_parser.tappedout._parse_deck(deck)

    assert result and all(result)


@pytest.mark.slow
@pytest.mark.parametrize('src', [
    'https://tappedout.net/mtg-decks/food-chain-sliver/',
])
def test_parse_deck_no_mock(src):
    result = mtg_parser.tappedout.parse_deck(src)

    assert result and all(result)
