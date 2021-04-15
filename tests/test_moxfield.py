#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests_mock
import pytest
import mtg_parser
from .utils import mock_response


@pytest.mark.parametrize('src, pattern, response', [
    [
        'https://www.moxfield.com/decks/7CBqQtCVKES6e49vKXfIBQ',
        r'https://.*?moxfield.com',
        'mock_moxfield_7CBqQtCVKES6e49vKXfIBQ',
    ],
])
def test_parse_deck(requests_mock, src, pattern, response):
    mock_response(requests_mock, pattern, response)

    result = mtg_parser.moxfield.parse_deck(src)

    assert result and all(result)


@pytest.mark.parametrize('deck', [{
    'commanders': {
        'Rasputin Dreamweaver': {
            'quantity': 1,
            'card': {
                'scryfall_id': 123,
            }
        },
    },
    'companions': {
        'Zirda, the Dawnwaker': {
            'quantity': 1,
            'card': {
                'scryfall_id': 456,
            }
        },
    },
    'mainboard': {
        'Sol Ring': {
            'quantity': 1,
            'card': {
                'scryfall_id': 789,
            }
        },
    },
}])
def test_internal_parse_deck(deck):
    result = mtg_parser.moxfield._parse_deck(deck)

    assert result and all(result)


@pytest.mark.slow
@pytest.mark.parametrize('src', [
    'https://www.moxfield.com/decks/7CBqQtCVKES6e49vKXfIBQ',
])
def test_parse_deck_no_mock(src):
    result = mtg_parser.moxfield.parse_deck(src)

    assert result and all(result)
