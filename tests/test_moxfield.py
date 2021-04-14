#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests_mock
import pytest
import mtg_parser
from .utils import mock_response


@pytest.mark.parametrize('src', [
    'https://api.moxfield.com/v2/decks/all/7CBqQtCVKES6e49vKXfIBQ',
])
def test_can_handle(src):
    assert mtg_parser.moxfield.can_handle(src)


@pytest.mark.parametrize('src, response', [
    [
        'https://api.moxfield.com/v2/decks/all/7CBqQtCVKES6e49vKXfIBQ',
        'mock_moxfield_7CBqQtCVKES6e49vKXfIBQ'
    ],
])
def test_parse_deck(requests_mock, src, response):
    mock_response(requests_mock, src, response)

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
