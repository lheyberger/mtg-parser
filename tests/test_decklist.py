#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser
from .utils import assert_objects_are_equal


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
        (1, "Atraxa, Praetors' Voice"),
        (1, "Imperial Seal"),
        (1, "Jeweled Lotus"),
        (1, "Lim-Dûl's Vault"),
        (1, "Llanowar Elves"),
        (3, "Brainstorm"),
    )

    cards = mtg_parser.decklist.parse_deck(decklist)

    for card, expected_card in zip(cards, expected_cards):
        assert card['quantity'] == expected_card[0]
        assert card['card_name'] == expected_card[1]


@pytest.mark.parametrize('string,expected', [
    [
        """//!Commander
        1 Atraxa, Praetors' Voice""",
        [{
            'quantity': 1,
            'card_name': "Atraxa, Praetors' Voice",
            'tags': ['Commander'],
        }],
    ],
    [
        """// Card Advantage
        3 Brainstorm #Draw #Card Advantage""",
        [{
            'quantity': 3,
            'card_name': 'Brainstorm',
            'tags': ['Card Advantage', 'Draw'],
        }],
    ],
    [
        """// Tutors
        1 Imperial Seal
        // Ramp
        1 Cultivate""",
        [{
            'quantity': 1,
            'card_name': 'Imperial Seal',
            'tags': ['Tutors'],
        }, {
            'quantity': 1,
            'card_name': 'Cultivate',
            'tags': ['Ramp'],
        }],
    ],
])
def test_decklist_sections(string, expected):
    result = mtg_parser.decklist.parse_deck(string)

    for card, expected_card in zip(result, expected):
        for key in expected_card.keys():
            assert_objects_are_equal(card[key], expected_card[key])


@pytest.mark.parametrize('decklist', [
    'https://www.archidekt.com/decks/1300410/'
    'https://deckstats.net/decks/30198/1297260-feather-the-redeemed',
    'https://www.moxfield.com/decks/7CBqQtCVKES6e49vKXfIBQ',
    'https://tappedout.net/mtg-decks/food-chain-sliver/',
    'https://www.mtggoldfish.com/deck/3862693',
])
def test_parse_decklist_fails(decklist):
    result = mtg_parser.decklist.parse_deck(decklist)

    assert result and not len(list(result))
