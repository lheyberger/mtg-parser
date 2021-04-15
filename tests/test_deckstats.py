#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests_mock
import pytest
import mtg_parser
from .utils import mock_response


@pytest.mark.parametrize('src, pattern, response', [
    [
        'https://deckstats.net/decks/30198/1297260-feather-the-redeemed',
        r'https://deckstats.net/',
        'mock_deckstats_30198_1297260-feather-the-redeemed',
    ],
])
def test_parse_deck(requests_mock, src, pattern, response):
    mock_response(requests_mock, pattern, response)

    result = mtg_parser.deckstats.parse_deck(src)

    assert result and all(result)


@pytest.mark.parametrize('deck', [{
    'sections': [{
        'cards': [{
            'amount': 1,
            'name': 'Rasputin Dreamweaver',
            'isCommander': True,
            'data': {
                'supertype_group_extended': 'creatures',
            },
        }]
    }, {
        'cards': [{
            'amount': 1,
            'name': 'Brainstorm',
            'data': {
                'supertype_group_extended': 'instants',
            },
        }, {
            'amount': 1,
            'name': 'Sol Ring',
            'data': {
                'supertype_group_extended': 'artifacts',
            }
        }]
    }]
}])
def test_internal_parse_deck(deck):
    result = mtg_parser.deckstats._parse_deck(deck)

    assert result and all(result)


@pytest.mark.slow
@pytest.mark.parametrize('src', [
    'https://deckstats.net/decks/30198/1297260-feather-the-redeemed',
])
def test_parse_deck_no_mock(src):
    result = mtg_parser.deckstats.parse_deck(src)

    assert result and all(result)
