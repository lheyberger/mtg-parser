#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import mtg_parser
from .utils import mock_response


@pytest.mark.parametrize('src', [
    'https://aetherhub.com/Deck/mtg-parser-3-amigos',
    'https://www.archidekt.com/decks/1365846/',
    'https://deckstats.net/decks/30198/2034245--mtg-parser-3-amigos',
    'https://www.moxfield.com/decks/Agzx8zsi5UezWBUX5hMJPQ',
    'https://www.mtggoldfish.com/deck/3935836',
    'https://mtgjson.com/api/v5/decks/BreedLethality_CM2.json',
    'https://scryfall.com/@gorila/decks/e7aceb4c-29d5-49f5-9a49-c24f64da264b',
    'https://tappedout.net/mtg-decks/mtg-parser-3-amigos/',
    'https://decks.tcgplayer.com/magic/commander/gorila/mtg-parser--3-amigos/1384198',
])
def test_can_handle_succdeeds(src):
    result = mtg_parser.can_handle(src)

    assert result


@pytest.mark.parametrize('src, mocked_responses', [
    [
        'https://aetherhub.com/Deck/mtg-parser-3-amigos',
        [{
            'pattern': r'https://aetherhub.com/Deck/(?!FetchMtgaDeckJson)',
            'response': 'mock_aetherhub_3-amigos',
        }, {
            'pattern': r'https://aetherhub.com/Deck/FetchMtgaDeckJson',
            'response': 'mock_aetherhub_3-amigos_json',
        }]
    ],
    [
        'https://www.archidekt.com/decks/1365846/',
        [{
            'pattern': r'https://www.archidekt.com/',
            'response': 'mock_archidekt_1365846_small',
        }],
    ],
    [
        'https://deckstats.net/decks/30198/2034245--mtg-parser-3-amigos',
        [{
            'pattern': r'https://deckstats.net/',
            'response': 'mock_deckstats_30198_2034245',
        }],
    ],
    [
        'https://www.moxfield.com/decks/Agzx8zsi5UezWBUX5hMJPQ',
        [{
            'pattern': r'https://.*?moxfield.com',
            'response': 'mock_moxfield_Agzx8zsi5UezWBUX5hMJPQ',
        }],
    ],
    [
        'https://www.mtggoldfish.com/deck/3935836',
        [{
            'pattern': r'https://www.mtggoldfish.com',
            'response': 'mock_mtggoldfish_3-amigos',
        }],
    ],
    [
        'https://scryfall.com/@gorila/decks/e7aceb4c-29d5-49f5-9a49-c24f64da264b',
        [{
            'pattern': r'(https?://)?(www\.)?scryfall\.com',
            'response': 'mock_scryfall_e7aceb4c-29d5-49f5-9a49-c24f64da264b',
        }],
    ],
    [
        'https://tappedout.net/mtg-decks/mtg-parser-3-amigos/',
        [{
            'pattern': r'https://tappedout.net/',
            'response': 'mock_tappedout_3-amigos',
        }],
    ],
    [
        'https://decks.tcgplayer.com/magic/commander/gorila/mtg-parser--3-amigos/1384198',
        [{
            'pattern': r'https://.*?tcgplayer.com',
            'response': 'mock_tcgplayer_3-amigos',
        }],
    ],
    [
        """
            1 Atraxa, Praetors' Voice
            1 Imperial Seal
            1 Jeweled Lotus (CMR) 319
            1 Lim-Dûl's Vault
            1 Llanowar Elves (M12) 182
            3 Brainstorm #Card Advantage #Draw
        """,
        [],
    ],
])
def test_parse_deck(requests_mock, src, mocked_responses):
    for mocked_response in mocked_responses:
        mock_response(
            requests_mock,
            mocked_response['pattern'],
            mocked_response['response'],
        )

    result = mtg_parser.parse_deck(src)

    assert result and all(result)


@pytest.mark.parametrize('src', [
    42,
])
def test_parse_deck_fails(src):
    result = mtg_parser.parse_deck(src)

    assert not result
