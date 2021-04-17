#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests_mock
import pytest
import mtg_parser
from .utils import mock_response


@pytest.mark.parametrize('src, pattern, response', [
    [
        'https://www.archidekt.com/decks/1300410/',
        r'https://www.archidekt.com/',
        'mock_archidekt_1300410_small',
    ],
    [
        'https://deckstats.net/decks/30198/1297260-feather-the-redeemed',
        r'https://deckstats.net/',
        'mock_deckstats_30198_1297260-feather-the-redeemed',
    ],
    [
        'https://www.moxfield.com/decks/7CBqQtCVKES6e49vKXfIBQ',
        r'https://.*?moxfield.com',
        'mock_moxfield_7CBqQtCVKES6e49vKXfIBQ',
    ],
    [
        'https://tappedout.net/mtg-decks/food-chain-sliver/',
        r'https://tappedout.net/',
        'mock_tappedout_food-chain-sliver',
    ],
    [
        'https://www.mtggoldfish.com/deck/3862693',
        r'https://www.mtggoldfish.com',
        'mock_mtggoldfish_3862693',
    ],
    [
        'https://decks.tcgplayer.com/magic/commander/playing-with-power-mtg/s08e08---kraum---tevesh/1383584',
        r'https://.*?tcgplayer.com',
        'mock_tcgplayer_s08e08_kraum_tevesh',
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
        None,
        None,
    ],
])
def test_parse_deck(requests_mock, src, pattern, response):
    mock_response(requests_mock, pattern, response)

    result = mtg_parser.parse_deck(src)

    assert result and all(result)


@pytest.mark.parametrize('src', [
    42,
])
def test_parse_deck_fails(src):
    result = mtg_parser.parse_deck(src)

    assert not result
