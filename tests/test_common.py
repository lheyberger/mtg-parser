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
    (mtg_parser.aetherhub.AetherhubDeckParser, aetherhub_deck_url),
    (mtg_parser.archidekt.ArchidektDeckParser, archidekt_deck_url),
    (mtg_parser.deckstats.DeckstatsDeckParser, deckstats_deck_url),
    (mtg_parser.moxfield.MoxfieldDeckParser, moxfield_deck_url),
    (mtg_parser.mtggoldfish.MtggoldfishDeckParser, mtggoldfish_deck_url),
    (mtg_parser.mtgjson.MtgjsonDeckParser, mtgjson_deck_url),
    (mtg_parser.scryfall.ScryfallDeckParser, scryfall_deck_url),
    (mtg_parser.tappedout.TappedoutDeckParser, tappedout_deck_url),
    (mtg_parser.tcgplayer.TcgplayerDeckParser, tcgplayer_infinite_deck_url),
    (mtg_parser.tcgplayer.TcgplayerDeckParser, tcgplayer_deck_url),
]


@pytest.mark.parametrize(('parser', 'deck_url'), TEST_DATA)
def test_can_handle_succdeeds(parser, deck_url):
    assert parser().can_handle(deck_url)


@pytest.mark.parametrize(('parser', 'deck_url'), TEST_DATA)
def test_can_handle_fails(parser, deck_url):
    assert not parser().can_handle(f"https://cannot_handle_this_url?{deck_url}")


@pytest.mark.parametrize(('parser', 'deck_url'), TEST_DATA)
def test_parse_deck_fails(parser, deck_url):
    assert not parser().parse_deck(f"https://cannot_handle_this_url?{deck_url}")


@pytest.mark.parametrize(('parser', 'deck_url'), TEST_DATA)
def test_parser_with_no_http_client(parser, deck_url):
    with pytest.raises(TypeError):
        parser().parse_deck(deck_url)


@pytest.mark.parametrize(('parser', 'deck_url'), TEST_DATA)
def test_parser_download_fails(monkeypatch, http_client_facade, parser, deck_url):
    subject = parser()
    monkeypatch.setattr(subject, "_download_deck", lambda _src, _client: None)
    with pytest.raises(RuntimeError):
        subject.parse_deck(deck_url, http_client_facade)


@pytest.mark.parametrize(('parser', 'deck_url'), TEST_DATA)
def test_parse_deck(http_client_facade, parser, deck_url):
    http_client_facade.read_mocks_from(Path('tests/mocks'))
    result = parser().parse_deck(deck_url, http_client_facade)
    assert_deck_is_valid(result)
