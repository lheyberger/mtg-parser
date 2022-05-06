#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser
from mtg_parser import Card


def test_mixed_decklist():
    decklist = """
        1 Atraxa, Praetors' Voice
        1 Imperial Seal
        1 Jeweled Lotus (CMR) 319
        1 Lim-Dûl's Vault
        1 Llanowar Elves (M12) 182
        3 Brainstorm #Card Advantage #Draw
    """
    expected_cards = (
        Card("Atraxa, Praetors' Voice", 1),
        Card("Imperial Seal", 1),
        Card("Jeweled Lotus", 1, extension='CMR', number='319'),
        Card("Lim-Dûl's Vault", 1),
        Card("Llanowar Elves", 1, extension='M12', number='182'),
        Card("Brainstorm", 3, tags=['card advantage', 'draw']),
    )

    cards = mtg_parser.decklist.parse_deck(decklist)

    for card, expected_card in zip(cards, expected_cards):
        assert card == expected_card


@pytest.mark.parametrize('string,expected', [
    [
        """//!Commander
        1 Atraxa, Praetors' Voice""",
        [
            Card("Atraxa, Praetors' Voice", 1, tags=['commander'])
        ],
    ],
    [
        """// Card Advantage
        3 Brainstorm #Draw #Card Advantage""",
        [
            Card('Brainstorm', 3, tags=['card advantage', 'draw'])
        ],
    ],
    [
        """// Tutors
        1 Imperial Seal
        // Ramp
        1 Cultivate""",
        [
            Card('Imperial Seal', 1, tags=['Tutors']),
            Card('Cultivate', 1, tags=['Ramp'])
        ],
    ],
])
def test_decklist_sections(string, expected):
    result = mtg_parser.decklist.parse_deck(string)

    for card, expected_card in zip(result, expected):
        assert card == expected_card


@pytest.mark.parametrize('decklist', [
    'https://www.archidekt.com/decks/1300410/'
    'https://deckstats.net/decks/30198/1297260-feather-the-redeemed',
    'https://www.moxfield.com/decks/7CBqQtCVKES6e49vKXfIBQ',
    'https://tappedout.net/mtg-decks/food-chain-sliver/',
    'https://www.mtggoldfish.com/deck/3862693',
])
def test_parse_decklist_fails(decklist):
    result = mtg_parser.decklist.parse_deck(decklist)

    assert not result or not any(result)
