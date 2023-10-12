#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import requests
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
        ['Minsc & Boo, Timeless Heroes'],
        'https://api.scryfall.com/cards/named?exact=Minsc+%26+Boo%2C+Timeless+Heroes',
    ],
    [
        ['Minsc & Boo, Timeless Heroes', None],
        'https://api.scryfall.com/cards/named?exact=Minsc+%26+Boo%2C+Timeless+Heroes',
    ],
    [
        ['Minsc & Boo, Timeless Heroes', None],
        'https://api.scryfall.com/cards/named?exact=Minsc+%26+Boo%2C+Timeless+Heroes',
    ],
])
def test_get_scryfall_url_name(parameters, expected):
    result = mtg_parser.utils.get_scryfall_url(*parameters)

    assert result == expected


@pytest.mark.parametrize('parameters, expected', [
    [
        ['Minsc & Boo, Timeless Heroes', 'clb'],
        'https://api.scryfall.com/cards/named?set=clb&exact=Minsc+%26+Boo%2C+Timeless+Heroes',
    ],
    [
        ['Minsc & Boo, Timeless Heroes', 'CLB'],
        'https://api.scryfall.com/cards/named?set=clb&exact=Minsc+%26+Boo%2C+Timeless+Heroes',
    ],
    [
        ['Minsc & Boo, Timeless Heroes', 'clb', None],
        'https://api.scryfall.com/cards/named?set=clb&exact=Minsc+%26+Boo%2C+Timeless+Heroes',
    ],
    [
        ['Minsc & Boo, Timeless Heroes', 'CLB', None],
        'https://api.scryfall.com/cards/named?set=clb&exact=Minsc+%26+Boo%2C+Timeless+Heroes',
    ],
])
def test_get_scryfall_url_name_set(parameters, expected):
    result = mtg_parser.utils.get_scryfall_url(*parameters)

    assert result == expected


@pytest.mark.parametrize('parameters, expected', [
    [
        ['Minsc & Boo, Timeless Heroes', 'clb', 285],
        'https://api.scryfall.com/cards/clb/285',
    ],
    [
        ['Minsc & Boo, Timeless Heroes', 'clb', '285'],
        'https://api.scryfall.com/cards/clb/285',
    ],
    [
        ['Hymn to Tourach', 'fem', '38a'],
        'https://api.scryfall.com/cards/fem/38a',
    ],
    [
        ['Arcane Signet', 'p30m', '1F★'],
        'https://api.scryfall.com/cards/p30m/1F%E2%98%85',
    ],
])
def test_get_scryfall_url_name_set_code(parameters, expected):
    result = mtg_parser.utils.get_scryfall_url(*parameters)

    assert result == expected


@pytest.mark.slow
@pytest.mark.parametrize('parameters', [
    ['Minsc & Boo, Timeless Heroes', ],
    ['Minsc & Boo, Timeless Heroes', 'clb'],
    ['Minsc & Boo, Timeless Heroes', 'CLB'],
    ['Minsc & Boo, Timeless Heroes', 'clb', 285],
    ['Minsc & Boo, Timeless Heroes', 'clb', '285'],
    ['Hymn to Tourach', ],
    ['Hymn to Tourach', 'fem'],
    ['Hymn to Tourach', 'fem', '38a'],
    ['Arcane Signet', ],
    ['Arcane Signet', 'p30m'],
    ['Arcane Signet', 'p30m', '1F★'],
])
def test_request_urls(parameters):
    url = mtg_parser.utils.get_scryfall_url(*parameters)

    requests.get(url).raise_for_status()
