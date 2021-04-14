#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser


@pytest.mark.slow
@pytest.mark.parametrize('deckstats_id', [
    '30198/1297260-feather-the-redeemed',
])
def test_get_deckstats_deck(deckstats_id):
    result = mtg_parser.get_deckstats_deck(deckstats_id)

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
def test_parse_deckstats_deck(deck):
    result = mtg_parser.parse_deckstats_deck(deck)

    assert result and all(result)
