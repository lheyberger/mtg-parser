#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser
from itertools import chain
from mtg_parser.card import Card
from .utils import mock_response
from .test_aetherhub import DECK_INFO as aetherhub_deck_info
from .test_archidekt import DECK_INFO as archidekt_deck_info
from .test_deckstats import DECK_INFO as deckstats_deck_info
from .test_moxfield import DECK_INFO as moxfield_deck_info
from .test_mtggoldfish import DECK_INFO as mtggoldfish_deck_info
from .test_mtgjson import DECK_INFO as mtgjson_deck_info
from .test_scryfall import DECK_INFO as scryfall_deck_info
from .test_tappedout import DECK_INFO as tappedout_deck_info
from .test_tcgplayer import DECK_INFO as tcgplayer_deck_info


@pytest.mark.parametrize('deck1,deck2', [
    [
        [
            Card('Brainstorm'),
            Card('Portent'),
            Card('Ponder'),
        ],
        [
            Card('Portent'),
            Card('Ponder'),
            Card('Opt'),
        ],
    ],
])
def test_diff(deck1, deck2):
    result = mtg_parser.diff(deck1, deck2)

    for _, value in result.items():
        assert value and all(value)


@pytest.mark.parametrize('deck_info', [
    aetherhub_deck_info,
    archidekt_deck_info,
    deckstats_deck_info,
    mtggoldfish_deck_info,
    # mtgjson_deck_info, ## not equal to others, by design
    scryfall_deck_info,
    tappedout_deck_info,
    # tcgplayer_deck_info, ## not equal to others yet
])
def test_diff_decks(requests_mock, deck_info):
    for mocked_response in chain(moxfield_deck_info['mocked_responses'], deck_info['mocked_responses']):
        mock_response(
            requests_mock,
            mocked_response['pattern'],
            mocked_response['response'],
        )

    deck1 = mtg_parser.parse_deck(moxfield_deck_info['url'])
    deck2 = mtg_parser.parse_deck(deck_info['url'])

    result = mtg_parser.diff(deck1, deck2)

    assert not result['deck1 - deck2']
    assert result['deck1 x deck2']
    assert not result['deck2 - deck1']
