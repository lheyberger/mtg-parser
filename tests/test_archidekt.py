#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser


@pytest.mark.parametrize('archidekt_id', [
    '1300410',
])
def test_get_archidekt_deck(archidekt_id):
    result = mtg_parser.get_archidekt_deck(archidekt_id)

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
def test_parse_archidekt_deck(deck):
    result = mtg_parser.parse_archidekt_deck(deck)

    assert result and all(result)
