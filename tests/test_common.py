#!/usr/bin/env python

import pytest
import mtg_parser
from pathlib import Path
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
    (mtg_parser.aetherhub.AetherhubDeckParser, aetherhub_deck_info),
    (mtg_parser.archidekt.ArchidektDeckParser, archidekt_deck_info),
    (mtg_parser.deckstats.DeckstatsDeckParser, deckstats_deck_info),
    (mtg_parser.moxfield.MoxfieldDeckParser, moxfield_deck_info),
    (mtg_parser.mtggoldfish.MtggoldfishDeckParser, mtggoldfish_deck_info),
    (mtg_parser.mtgjson.MtgjsonDeckParser, mtgjson_deck_info),
    (mtg_parser.scryfall.ScryfallDeckParser, scryfall_deck_info),
    (mtg_parser.tappedout.TappedoutDeckParser, tappedout_deck_info),
    (mtg_parser.tcgplayer.TcgplayerDeckParser, tcgplayer_infinite_deck_info),
    (mtg_parser.tcgplayer.TcgplayerDeckParser, tcgplayer_deck_info),
]


@pytest.mark.parametrize(('parser', 'deck_info'), TEST_DATA)
def test_can_handle_succdeeds(parser, deck_info):
    assert parser().can_handle(deck_info['url'])


@pytest.mark.parametrize(('parser', 'deck_info'), TEST_DATA)
def test_can_handle_fails(parser, deck_info):
    assert not parser().can_handle(f"https://cannot_handle_this_url?{deck_info['url']}")


@pytest.mark.parametrize(('parser', 'deck_info'), TEST_DATA)
def test_parse_deck_fails(parser, deck_info):
    assert not parser().parse_deck(f"https://cannot_handle_this_url?{deck_info['url']}")


@pytest.mark.parametrize(('parser', 'deck_info'), TEST_DATA)
def test_parser_with_no_http_client(parser, deck_info):
    with pytest.raises(TypeError):
        parser().parse_deck(deck_info['url'])


@pytest.mark.parametrize(('parser', 'deck_info'), TEST_DATA)
def test_parser_download_fails(monkeypatch, http_client_facade, parser, deck_info):
    subject = parser()
    monkeypatch.setattr(subject, "_download_deck", lambda _src, _client: None)
    with pytest.raises(RuntimeError):
        subject.parse_deck(deck_info['url'], http_client_facade)


@pytest.mark.parametrize(('parser', 'deck_info'), TEST_DATA)
def test_parse_deck(http_client_facade, parser, deck_info):
    http_client_facade.read_mocks_from(Path('tests/mocks'))
    result = parser().parse_deck(deck_info['url'], http_client_facade)
    assert_deck_is_valid(result)
