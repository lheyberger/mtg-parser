#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests_mock
import pytest
import mtg_parser
from .utils import mock_response


@pytest.mark.parametrize('deck1,deck2', [
    [
        [
            {'card_name': 'Brainstorm'},
            {'card_name': 'Portent'},
            {'card_name': 'Ponder'},
        ],
        [
            {'card_name': 'Portent'},
            {'card_name': 'Ponder'},
            {'card_name': 'Opt'},
        ],
    ],
])
def test_diff(deck1, deck2):
    result = mtg_parser.diff(deck1, deck2)

    for _, value in result.items():
        assert value and all(value)


@pytest.mark.parametrize('src1, response1, src2, response2', [
    [
        'https://www.archidekt.com/api/decks/1300410/small/',
        'mock_archidekt_1300410_small',
        'https://deckstats.net/decks/30198/1297260-feather-the-redeemed',
        'mock_deckstats_30198_1297260-feather-the-redeemed',
    ],
])
def test_diff_decks(requests_mock, src1, response1, src2, response2):
    mock_response(requests_mock, src1, response1)
    deck1 = mtg_parser.parse_deck(src1)
    mock_response(requests_mock, src2, response2)
    deck2 = mtg_parser.parse_deck(src2)

    result = mtg_parser.diff(deck1, deck2)

    for _, value in result.items():
        assert value and all(value)
