#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser


@pytest.mark.parametrize('moxfield_id', [
    '7CBqQtCVKES6e49vKXfIBQ',
])
def test_get_moxfield_deck(moxfield_id):
    result = mtg_parser.get_moxfield_deck(moxfield_id)

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
def test_parse_moxfield_deck(deck):
    result = mtg_parser.parse_moxfield_deck(deck)

    assert result and all(result)
