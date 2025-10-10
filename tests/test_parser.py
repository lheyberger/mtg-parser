#!/usr/bin/env python

import pytest
import mtg_parser
from .test_aetherhub import DECK_INFO as aetherhub_deck_info
from .test_archidekt import DECK_INFO as archidekt_deck_info
from .test_deckstats import DECK_INFO as deckstats_deck_info
from .test_moxfield import DECK_INFO as moxfield_deck_info
from .test_mtggoldfish import DECK_INFO as mtggoldfish_deck_info
from .test_mtgjson import DECK_INFO as mtgjson_deck_info
from .test_scryfall import DECK_INFO as scryfall_deck_info
from .test_tappedout import DECK_INFO as tappedout_deck_info
from .test_tcgplayer_infinite import DECK_INFO as tcgplayer_infinite_deck_info
from .test_tcgplayer import DECK_INFO as tcgplayer_deck_info
from .utils import assert_deck_is_valid


TEST_DATA = [
    aetherhub_deck_info,
    archidekt_deck_info,
    deckstats_deck_info,
    moxfield_deck_info,
    mtggoldfish_deck_info,
    mtgjson_deck_info,
    scryfall_deck_info,
    tappedout_deck_info,
    tcgplayer_infinite_deck_info,
    tcgplayer_deck_info,
]


@pytest.mark.parametrize('deck_info', TEST_DATA)
def test_can_handle_succeeds(deck_info):
    assert mtg_parser.can_handle(deck_info['url'])


@pytest.mark.parametrize('deck_info', TEST_DATA)
def test_can_handle_fails(deck_info):
    assert not mtg_parser.can_handle(f"https://cannot_handle_this_url?{deck_info['url']}")


@pytest.mark.parametrize('deck_info', TEST_DATA)
def test_parse_deck_fails(deck_info):
    assert not mtg_parser.parse_deck(f"https://cannot_handle_this_url?{deck_info['url']}")


@pytest.mark.parametrize('deck_info', [
    aetherhub_deck_info,
    archidekt_deck_info,
    deckstats_deck_info,
    moxfield_deck_info,
    mtggoldfish_deck_info,
    mtgjson_deck_info,
    scryfall_deck_info,
    tappedout_deck_info,
    tcgplayer_infinite_deck_info,
    tcgplayer_deck_info,
])
def test_parse_deck(respx_mock, http_client_facade, deck_info):
    for mocked_response in deck_info['mocked_responses']:
        respx_mock(mocked_response['pattern'], mocked_response['response'])

    result = mtg_parser.parse_deck(deck_info['url'], http_client_facade)

    assert result
    assert all(result)


@pytest.mark.parametrize('decklist', [
    """
        1 Atraxa, Praetors' Voice
        1 Imperial Seal
        1 Jeweled Lotus (CMR) 319
        1 Lim-Dûl's Vault
        1 Llanowar Elves (M12) 182
        3 Brainstorm #Card Advantage #Draw
    """,
])
def test_parse_deck_decklist(decklist):
    result = mtg_parser.parse_deck(decklist)

    assert result
    assert all(result)


@pytest.mark.slow
@pytest.mark.parametrize('deck_info', [
    aetherhub_deck_info,
    archidekt_deck_info,
    deckstats_deck_info,
    moxfield_deck_info,
    mtggoldfish_deck_info,
    mtgjson_deck_info,
    scryfall_deck_info,
    tappedout_deck_info,
    tcgplayer_infinite_deck_info,
    tcgplayer_deck_info,
])
def test_parse_deck_no_mock(http_client_facade, deck_info):
    result = mtg_parser.parse_deck(deck_info['url'], http_client_facade)
    assert_deck_is_valid(result)
