#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser
from mtg_parser.card import Card
from .utils import mock_response


@pytest.mark.parametrize('deck1,deck2', [
    [
        [
            Card('Brainstorm'),
            Card('Portent'),
            Card('Ponder'),
        ],
        [
            Card('Portent'),
            Card('Ponder'),
            Card('Opt'),
        ],
    ],
])
def test_diff(deck1, deck2):
    result = mtg_parser.diff(deck1, deck2)

    for _, value in result.items():
        assert value and all(value)


@pytest.mark.parametrize('src1, response1, src2, response2', [
    [
        'https://www.archidekt.com/decks/1365846/',
        [{
            'pattern': r'https://www.archidekt.com/',
            'response': 'mock_archidekt_1365846_small',
        }],
        'https://deckstats.net/decks/30198/2034245--mtg-parser-3-amigos',
        [{
            'pattern': r'https://deckstats.net/',
            'response': 'mock_deckstats_30198_2034245',
        }],
    ],
])
def test_diff_decks(requests_mock, src1, response1, src2, response2):
    for mocked_queries in [response1, response2]:
        for query in mocked_queries:
            mock_response(requests_mock, query['pattern'], query['response'])
    deck1 = mtg_parser.parse_deck(src1)
    deck2 = mtg_parser.parse_deck(src2)

    result = mtg_parser.diff(deck1, deck2)

    assert not result['deck1 - deck2']
    assert result['deck1 x deck2']
    assert not result['deck2 - deck1']
