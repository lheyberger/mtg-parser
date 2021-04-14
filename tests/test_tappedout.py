#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests_mock
import pytest
import mtg_parser
from .utils import mock_response


@pytest.mark.parametrize('src', [
    'https://tappedout.net/mtg-decks/food-chain-sliver/',
])
def test_can_handle(src):
    assert mtg_parser.tappedout.can_handle(src)


@pytest.mark.parametrize('src, response', [
    [
        'https://tappedout.net/mtg-decks/food-chain-sliver/',
        'mock_tappedout_food-chain-sliver'
    ],
])
def test_parse_deck(requests_mock, src, response):
    mock_response(requests_mock, src, response)

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
