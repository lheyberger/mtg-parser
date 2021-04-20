#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser


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
def test_Card(card):
    result = mtg_parser.Card(**card)

    assert result.__repr__()
    assert result.__str__()
