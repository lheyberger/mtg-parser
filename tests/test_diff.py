#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser
from tabulate import tabulate


@pytest.mark.parametrize('deck1,deck2', [
    [
        [
            {'card_name': 'Brainstorm'},
            {'card_name': 'Portent'},
            {'card_name': 'Ponder'},
        ],
        [
            {'card_name': 'Portent'},
            {'card_name': 'Ponder'}, 
            {'card_name': 'Opt'}, 
        ],
    ],
])
def test_diff(deck1, deck2):
    result = mtg_parser.diff(deck1, deck2)

    for key, value in result.items():
        assert value and all(value)


@pytest.mark.verbose
def test_diff_moxfield_decks():
    deck1 = '7CBqQtCVKES6e49vKXfIBQ'
    deck1 = mtg_parser.get_moxfield_deck(deck1)
    deck1 = mtg_parser.parse_moxfield_deck(deck1)

    deck2 = 'jT8Y9X4tlUmeNZ2AjkD1Vg'
    deck2 = mtg_parser.get_moxfield_deck(deck2)
    deck2 = mtg_parser.parse_moxfield_deck(deck2)

    result = mtg_parser.diff(deck1, deck2, differences_only=True)

    print(tabulate(result, headers='keys'))
