#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser
from .asserts import assert_objects_are_equal


@pytest.mark.parametrize('symbol,string,expected', [
    [
        mtg_parser.gramar.QUANTITY,
        '1',
        {'quantity': 1},
    ],
    [
        mtg_parser.gramar.QUANTITY,
        '2',
        {'quantity': 2},
    ],
    [
        mtg_parser.gramar.COLLECTOR_NUMBER,
        '72',
        {'collector_number': '72'},
    ],
    [
        mtg_parser.gramar.COLLECTOR_NUMBER,
        '238',
        {'collector_number': '238'},
    ],
    [
        mtg_parser.gramar.EXTENSION,
        'USG',
        {'extension': 'USG'},
    ],
    [
        mtg_parser.gramar.EXTENSION,
        'J16',
        {'extension': 'J16'},
    ],
    [
        mtg_parser.gramar.TAG,
        '#Finish',
        {'tags': ['Finish']},
    ],
    [
        mtg_parser.gramar.TAG,
        '#Extra Turn',
        {'tags': ['Extra Turn']},
    ],
    [
        mtg_parser.gramar.TAG,
        '#!Ramp',
        {'tags': ['Ramp']},
    ],
    [
        mtg_parser.gramar.TAG,
        '#!Card Advantage',
        {'tags': ['Card Advantage']}
    ],
    [
        mtg_parser.gramar.TAG,
        '#!Card Advantage',
        {'tags': ['Card Advantage']}
    ],
    [
        mtg_parser.gramar.MTGA_EXTENSION,
        '(USG)',
        {'extension': 'USG'},
    ],
    [
        mtg_parser.gramar.MTGA_EXTENSION,
        '(J16)',
        {'extension': 'J16'},
    ],
    [
        mtg_parser.gramar.COMMENT_LINE,
        '//Card Advantage',
        {'comment': 'Card Advantage'},
    ],
    [
        mtg_parser.gramar.COMMENT_LINE,
        '// Card Advantage',
        {'comment': 'Card Advantage'},
    ],
])
def test_gramar_succeeds(symbol, string, expected):
    result = symbol.parseString(string).asDict()

    assert_objects_are_equal(result, expected)


@pytest.mark.parametrize('quantity', [
    ('1', {'quantity': 1}),
    ('20', {'quantity': 20}),
])
@pytest.mark.parametrize('card_name', [
    ('Gilded Drake', {'card_name': 'Gilded Drake'}),
    ('Lim-Dûl\'s Vault', {'card_name': 'Lim-Dûl\'s Vault'}),
    ('Atraxa, Praetors\' Voice', {'card_name': 'Atraxa, Praetors\' Voice'}),
    ('Response / Resurgence', {'card_name': 'Response / Resurgence'}),
    ('Response // Resurgence', {'card_name': 'Response // Resurgence'}),
])
@pytest.mark.parametrize('tags', [
    ('#Finish', {'tags': ['Finish']}),
    ('#Extra Turn', {'tags': ['Extra Turn']}),
    ('#!Ramp', {'tags': ['Ramp']}),
    ('#!Card Advantage', {'tags': ['Card Advantage']}),
    ('#!Ramp #Draw', {'tags': ['Ramp', 'Draw']}),
])
def test_mtgo_line(quantity, card_name, tags):
    symbol = mtg_parser.gramar.MTGO_LINE
    expected = {**quantity[1], **card_name[1], **tags[1]}
    string = ' '.join((quantity[0], card_name[0], tags[0]))

    result = symbol.parseString(string).asDict()

    assert_objects_are_equal(result, expected)


@pytest.mark.parametrize('quantity', [
    ('1', {'quantity': 1}),
    ('20', {'quantity': 20}),
])
@pytest.mark.parametrize('card_name', [
    ('Gilded Drake', {'card_name': 'Gilded Drake'}),
    ('Lim-Dûl\'s Vault', {'card_name': 'Lim-Dûl\'s Vault'}),
    ('Atraxa, Praetors\' Voice', {'card_name': 'Atraxa, Praetors\' Voice'}),
    ('Response / Resurgence', {'card_name': 'Response / Resurgence'}),
    ('Response // Resurgence', {'card_name': 'Response // Resurgence'}),
])
@pytest.mark.parametrize('extension', [
    ('(J16)', {'extension': 'J16'}),
    ('(TTSR)', {'extension': 'TTSR'}),
])
@pytest.mark.parametrize('collector_number', [
    ('72', {'collector_number': '72'}),
    ('237a', {'collector_number': '237a'}),
])
@pytest.mark.parametrize('tags', [
    ('#Finish', {'tags': ['Finish']}),
    ('#Extra Turn', {'tags': ['Extra Turn']}),
    ('#!Ramp', {'tags': ['Ramp']}),
    ('#!Card Advantage', {'tags': ['Card Advantage']}),
    ('#!Ramp #Draw', {'tags': ['Ramp', 'Draw']}),
])
def test_mtga_line(quantity, card_name, extension, collector_number, tags):
    symbol = mtg_parser.gramar.MTGA_LINE
    expected = {
        **quantity[1],
        **card_name[1],
        **extension[1],
        **collector_number[1],
        **tags[1],
    }
    string = ' '.join((
        quantity[0],
        card_name[0],
        extension[0],
        collector_number[0],
        tags[0]
    ))

    result = symbol.parseString(string).asDict()

    assert_objects_are_equal(result, expected)


@pytest.mark.parametrize('string,expected', [
    [
        '1 Gilded Drake (USG) 76',
        {
            'quantity': 1,
            'card_name': 'Gilded Drake',
            'extension': 'USG',
            'collector_number': '76'
        },
    ],
    [
        '1 Gitaxian Probe',
        {
            'quantity': 1,
            'card_name': 'Gitaxian Probe',
        },
    ],
])
def test_line(string, expected):
    symbol = mtg_parser.gramar.LINE

    result = symbol.parseString(string).asDict()

    assert_objects_are_equal(result, expected)
