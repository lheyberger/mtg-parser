#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from mtg_parser import Card


@pytest.mark.parametrize('card', [
    {
        'quantity': '1',
        'name': 'Barkchannel Pathway // Tidechannel Pathway',
    },
    {
        'quantity': 1,
        'name': 'Gitaxian Probe',
        'extension': 'NPH',
    },
    {
        'quantity': 1,
        'name': 'Gilded Drake',
        'extension': 'USG',
        'number': '76'
    },
    {
        'quantity': '1',
        'name': 'Brainstorm',
        'tags': ['Instant', None, 'Card Advantage', 42]
    },
])
def test_card(card):
    result = Card(**card)

    assert repr(result)
    assert str(result)


@pytest.mark.parametrize('left, right', [
    [
        Card('Sol Ring'),
        Card('Sol Ring'),
    ],
    [
        Card('Sol Ring', quantity=1),
        Card('Sol Ring', quantity=1),
    ],
    [
        Card('Sol Ring', extension='mps'),
        Card('Sol Ring', extension='mps'),
    ],
    [
        Card('Sol Ring', number='24'),
        Card('Sol Ring', number='24'),
    ],
    [
        Card('Sol Ring', tags=['Ramp']),
        Card('Sol Ring', tags=['Ramp']),
    ],
    [
        Card('Sol Ring', tags=['Artifact', 'Ramp']),
        Card('Sol Ring', tags=['Artifact', 'Ramp']),
    ],
])
def test_card_strictly_equals(left, right):
    assert left == right
    assert left <= right
    assert left >= right


@pytest.mark.parametrize('left, right', [
    [
        Card('Sol Ring'),
        Card('Sol Ring', quantity=1),
    ],
    [
        Card('Sol Ring', quantity=1),
        Card('Sol Ring', quantity='1'),
    ],
    [
        Card('Sol Ring', number=24),
        Card('Sol Ring', number='24'),
    ],
    [
        Card('Sol Ring', tags=['RAMP']),
        Card('Sol Ring', tags=['ramp']),
    ],
    [
        Card('Sol Ring', tags=['Artifact', 'Ramp']),
        Card('Sol Ring', tags=['Ramp', 'Artifact']),
    ],
    [
        Card('Sol Ring', tags=['ARTIFACT', 'Ramp']),
        Card('Sol Ring', tags=['RAMP', 'Artifact']),
    ],
])
def test_card_equals(left, right):
    assert left == right
    assert left <= right
    assert left >= right


@pytest.mark.parametrize('left, right', [
    [
        Card('sol ring'),
        Card('SOL RING'),
    ],
    [
        Card('Sol Ring', quantity=1),
        Card('Sol Ring', quantity=2),
    ],
    [
        Card('Sol Ring', extension='lea'),
        Card('Sol Ring', extension='mps'),
    ],
    [
        Card('Sol Ring', extension='MPS'),
        Card('Sol Ring', extension='mps'),
    ],
    [
        Card('Sol Ring', number='24a'),
        Card('Sol Ring', number='24A'),
    ],
    [
        Card('Sol Ring', number='1'),
        Card('Sol Ring', number='2'),
    ],
    [
        Card('Sol Ring', tags=['Ramp']),
        Card('Sol Ring', tags=['Artifact']),
    ],
    [
        Card('Sol Ring', tags=['Ramp']),
        Card('Sol Ring', tags=['Artifact', 'Ramp']),
    ],
])
def test_card_not_equals(left, right):
    assert left != right
    assert not left == right


@pytest.mark.parametrize('left, right', [
    [
        Card('Brainstorm'),
        Card('Sol Ring'),
    ],
    [
        Card('Sol Ring', quantity=1),
        Card('Sol Ring', quantity=2),
    ],
    [
        Card('Sol Ring', extension='C17'),
        Card('Sol Ring', extension='C18'),
    ],
    [
        Card('Sol Ring', number='10'),
        Card('Sol Ring', number='20'),
    ],
    [
        Card('Sol Ring', extension='MPS'),
        Card('Sol Ring', extension='mps'),
    ],
    [
        Card('Sol Ring', number='24A'),
        Card('Sol Ring', number='24a'),
    ],
    # [
    #     Card('Sol Ring', tags=['Artifact']),
    #     Card('Sol Ring', tags=['Ramp']),
    # ],
])
def test_card_strictly_less_than(left, right):
    assert left < right
    assert left <= right
    assert left != right
    assert not left > right
    assert not left >= right


@pytest.mark.parametrize('left, right', [
    [
        Card('Sol Ring'),
        Card('Brainstorm'),
    ],
    [
        Card('Sol Ring', quantity=2),
        Card('Sol Ring', quantity=1),
    ],
    [
        Card('Sol Ring', extension='C18'),
        Card('Sol Ring', extension='C17'),
    ],
    [
        Card('Sol Ring', number='20'),
        Card('Sol Ring', number='10'),
    ],
    # [
    #     Card('Sol Ring', tags=['Ramp']),
    #     Card('Sol Ring', tags=['Artifact']),
    # ],
])
def test_card_strictly_greater_than(left, right):
    assert left > right
    assert left >= right
    assert left != right
    assert not left < right
    assert not left <= right
