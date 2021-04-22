#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests_mock
import pytest
import mtg_parser
from .utils import mock_response


@pytest.mark.parametrize('src, mocked_responses', [
    [
        'https://aetherhub.com/Deck/thrasios-and-tymna---efficient',
        [{
            'pattern': r'https://aetherhub.com/Deck/(?!FetchMtgaDeckJson)',
            'response': 'mock_aetherhub_489549',
        }, {
            'pattern': r'https://aetherhub.com/Deck/FetchMtgaDeckJson',
            'response': 'mock_aetherhub_489549_json',
        }],
    ],
    [
        'https://www.archidekt.com/decks/1300410/',
        [{
            'pattern': r'https://www.archidekt.com/',
            'response': 'mock_archidekt_1300410_small',
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
        'https://tappedout.net/mtg-decks/mtg-parser-3-amigos/',
        [{
            'pattern': r'https://tappedout.net/',
            'response': 'mock_tappedout_3-amigos',
        }],
    ],
    [
        'https://www.mtggoldfish.com/deck/3862693',
        [{
            'pattern': r'https://www.mtggoldfish.com',
            'response': 'mock_mtggoldfish_3862693',
        }],
    ],
    [
        'https://decks.tcgplayer.com/magic/commander/playing-with-power-mtg/s08e08---kraum---tevesh/1383584',
        [{
            'pattern': r'https://.*?tcgplayer.com',
            'response': 'mock_tcgplayer_s08e08_kraum_tevesh',
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
