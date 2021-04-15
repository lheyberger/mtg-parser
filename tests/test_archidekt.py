#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests_mock
import pytest
import mtg_parser
from .utils import mock_response


@pytest.mark.parametrize('src', [
    'https://www.archidekt.com/api/decks/1300410/'
])
def test_can_handle(src):
    assert mtg_parser.archidekt.can_handle(src)


@pytest.mark.parametrize('src, response', [
    [
        'https://www.archidekt.com/api/decks/1300410/small/',
        'mock_archidekt_1300410_small',
    ],
])
def test_parse_deck(requests_mock, src, response):
    mock_response(requests_mock, src, response)

    result = mtg_parser.archidekt.parse_deck(src)

    assert result and all(result)


@pytest.mark.parametrize('deck', [{
    'categories': [
        {'includedInDeck': True, 'name': 'Commander'},
    ],
    'cards': [{
        'quantity': 1,
        'card': {
            'oracleCard': {'name': 'Urza, Lord High Artificer'},
            'edition': {'editioncode': 'mh1'},
            'collectorNumber': '75',
        },
        'categories': ['Commander'],
    }],
}])
def test_internal_parse_deck(deck):
    result = mtg_parser.archidekt._parse_deck(deck)

    assert result and all(result)


@pytest.mark.parametrize('src', [
    'https://www.archidekt.com/api/decks/1300410/small/',
])
def test_parse_deck(src):
    result = mtg_parser.archidekt.parse_deck(src)

    print(len(list(result)))
    assert result and all(result)
