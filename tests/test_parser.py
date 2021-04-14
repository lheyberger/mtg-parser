#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests_mock
import pytest
import mtg_parser
from .utils import mock_response


@pytest.mark.parametrize('src', [
    'https://www.archidekt.com/api/decks/1300410/',
    'https://deckstats.net/decks/30198/1297260-feather-the-redeemed',
    'https://api.moxfield.com/v2/decks/all/7CBqQtCVKES6e49vKXfIBQ',
    'https://tappedout.net/mtg-decks/food-chain-sliver/',
    """
        1 Atraxa, Praetors' Voice
        1 Imperial Seal
        1 Jeweled Lotus (CMR) 319
        1 Lim-Dûl's Vault
        1 Llanowar Elves (M12) 182
        3 Brainstorm #Card Advantage #Draw
    """,
])
def test_can_handle(src):
    assert mtg_parser.can_handle(src)


@pytest.mark.parametrize('src', [
    42,
])
def test_can_handle_fails(src):
    assert not mtg_parser.can_handle(src)


@pytest.mark.parametrize('src, response', [
    [
        'https://www.archidekt.com/api/decks/1300410/',
        'mock_archidekt_1300410',
    ],
    [
        'https://deckstats.net/decks/30198/1297260-feather-the-redeemed',
        'mock_deckstats_30198_1297260-feather-the-redeemed',
    ],
    [
        'https://api.moxfield.com/v2/decks/all/7CBqQtCVKES6e49vKXfIBQ',
        'mock_moxfield_7CBqQtCVKES6e49vKXfIBQ'
    ],
    [
        'https://tappedout.net/mtg-decks/food-chain-sliver/',
        'mock_tappedout_food-chain-sliver'
    ],
    [
        """
            1 Atraxa, Praetors' Voice
            1 Imperial Seal
            1 Jeweled Lotus (CMR) 319
            1 Lim-Dûl's Vault
            1 Llanowar Elves (M12) 182
            3 Brainstorm #Card Advantage #Draw
        """,
        None
    ],
])
def test_parse_deck(requests_mock, src, response):
    mock_response(requests_mock, src, response)

    result = mtg_parser.parse_deck(src)

    assert result and all(result)


@pytest.mark.parametrize('src', [
    42,
])
def test_parse_deck_fails(src):
    result = mtg_parser.parse_deck(src)

    assert not result
