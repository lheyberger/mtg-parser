#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from mtg_parser import add_scryfall_urls


@pytest.mark.parametrize('cards', [
    [{
        'card_name': "Atraxa, Praetors' Voice"
    }],
    [{
        'card_name': "Brainstorm"
    }],
    [{
        'extension': "CMR", 'collector_number': "319"
    }],
    [{
        'extension': "M12", 'collector_number': "182"
    }],
    [{
        'card_name': "Jeweled Lotus",
        'extension': "CMR",
        'collector_number': "319"
    }],
    [{
        'card_name': "Llanowar Elves",
        'extension': "M12",
        'collector_number': "182"
    }],
])
def test_add_scryfall_urls(cards):
    result = add_scryfall_urls(cards)

    for card in result:
        assert 'scryfall_url' in card
