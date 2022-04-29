#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser


@pytest.mark.parametrize('parameters, expected', [
    [
        [],
        'https://api.scryfall.com/cards',
    ],
    [
        [None],
        'https://api.scryfall.com/cards',
    ],
    [
        [None, None],
        'https://api.scryfall.com/cards',
    ],
    [
        [None, None, None],
        'https://api.scryfall.com/cards',
    ],
])
def test_get_scryfall_url_no_parameters(parameters, expected):
    result = mtg_parser.utils.get_scryfall_url(*parameters)

    assert result == expected


@pytest.mark.parametrize('parameters, expected', [
    [
        ['Najeela, the Blade-Blossom'],
        'https://api.scryfall.com/cards/named?exact=Najeela,+the+Blade-Blossom',
    ],
    [
        ['Najeela, the Blade-Blossom', None],
        'https://api.scryfall.com/cards/named?exact=Najeela,+the+Blade-Blossom',
    ],
    [
        ['Najeela, the Blade-Blossom', None, None],
        'https://api.scryfall.com/cards/named?exact=Najeela,+the+Blade-Blossom',
    ],
])
def test_get_scryfall_url_name(parameters, expected):
    result = mtg_parser.utils.get_scryfall_url(*parameters)

    assert result == expected


@pytest.mark.parametrize('parameters, expected', [
    [
        ['Najeela, the Blade-Blossom', 'bbd'],
        'https://api.scryfall.com/cards/named?set=bbd&exact=Najeela,+the+Blade-Blossom',
    ],
    [
        ['Najeela, the Blade-Blossom', 'BBD'],
        'https://api.scryfall.com/cards/named?set=bbd&exact=Najeela,+the+Blade-Blossom',
    ],
    [
        ['Najeela, the Blade-Blossom', 'BBD', None],
        'https://api.scryfall.com/cards/named?set=bbd&exact=Najeela,+the+Blade-Blossom',
    ],
])
def test_get_scryfall_url_name_set(parameters, expected):
    result = mtg_parser.utils.get_scryfall_url(*parameters)

    assert result == expected


@pytest.mark.parametrize('parameters, expected', [
    [
        ['Najeela, the Blade-Blossom', 'BBD', 62],
        'https://api.scryfall.com/cards/bbd/62',
    ],
    [
        ['Najeela, the Blade-Blossom', 'bbd', 62],
        'https://api.scryfall.com/cards/bbd/62',
    ],
    [
        ['Najeela, the Blade-Blossom', 'bbd', 62],
        'https://api.scryfall.com/cards/bbd/62',
    ],
    [
        ['Hymn to Tourach', 'FEM', '38A'],
        'https://api.scryfall.com/cards/fem/38a',
    ],
    [
        ['Hymn to Tourach', 'fem', '38a'],
        'https://api.scryfall.com/cards/fem/38a',
    ],
])
def test_get_scryfall_url_name_set_code(parameters, expected):
    result = mtg_parser.utils.get_scryfall_url(*parameters)

    assert result == expected
