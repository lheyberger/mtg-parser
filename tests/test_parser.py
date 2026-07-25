#!/usr/bin/env python

import pytest
import mtg_parser
from pathlib import Path
from .test_aetherhub import DECK_URL as aetherhub_deck_url
from .test_archidekt import DECK_URL as archidekt_deck_url
from .test_deckstats import DECK_URL as deckstats_deck_url
from .test_moxfield import DECK_URL as moxfield_deck_url
from .test_mtggoldfish import DECK_URL as mtggoldfish_deck_url
from .test_mtgjson import DECK_URL as mtgjson_deck_url
from .test_scryfall import DECK_URL as scryfall_deck_url
from .test_tappedout import DECK_URL as tappedout_deck_url
from .test_tcgplayer_infinite import DECK_URL as tcgplayer_infinite_deck_url
from .test_tcgplayer import DECK_URL as tcgplayer_deck_url
from .utils import assert_deck_is_valid


TEST_DATA = [
    aetherhub_deck_url,
    archidekt_deck_url,
    deckstats_deck_url,
    moxfield_deck_url,
    mtggoldfish_deck_url,
    mtgjson_deck_url,
    scryfall_deck_url,
    tappedout_deck_url,
    tcgplayer_infinite_deck_url,
    tcgplayer_deck_url,
]


@pytest.mark.parametrize('deck_url', TEST_DATA)
def test_can_handle_succeeds(deck_url):
    assert mtg_parser.can_handle(deck_url)


@pytest.mark.parametrize('deck_url', TEST_DATA)
def test_can_handle_fails(deck_url):
    assert not mtg_parser.can_handle(f"https://cannot_handle_this_url?{deck_url}")


@pytest.mark.parametrize('deck_url', TEST_DATA)
def test_parse_deck_fails(deck_url):
    assert not mtg_parser.parse_deck(f"https://cannot_handle_this_url?{deck_url}")


@pytest.mark.parametrize('deck_url', TEST_DATA)
def test_parse_deck(http_client_facade, deck_url):
    http_client_facade.read_mocks_from(Path('tests/mocks'))
    result = mtg_parser.parse_deck(deck_url, http_client_facade)
    assert_deck_is_valid(result)


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
